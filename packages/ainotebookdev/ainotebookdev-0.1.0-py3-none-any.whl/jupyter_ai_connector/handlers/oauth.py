"""OAuth authentication handlers for Auth0.

Implements the OAuth 2.0 Authorization Code flow with PKCE.
"""

import base64
import json
import logging
from typing import Any

from jupyter_server.base.handlers import APIHandler
import httpx

from ..auth.token_store import TokenStore

logger = logging.getLogger(__name__)


def _get_public_origin(request) -> str:
    """Resolve public origin, honoring common proxy headers."""
    proto = request.headers.get("X-Forwarded-Proto", request.protocol)
    host = request.headers.get("X-Forwarded-Host", request.host)
    if proto and "," in proto:
        proto = proto.split(",", 1)[0].strip()
    if host and "," in host:
        host = host.split(",", 1)[0].strip()
    return f"{proto}://{host}"

# Callback HTML template - sends auth code back to parent window
CALLBACK_HTML = """<!DOCTYPE html>
<html>
<head>
    <title>Authentication</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: #f5f5f5;
        }
        .message {
            text-align: center;
            padding: 2rem;
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .error { color: #e74c3c; }
    </style>
</head>
<body>
    <div class="message">
        <div class="spinner" id="spinner"></div>
        <p id="status">Completing sign in...</p>
    </div>
    <script>
        (function() {
            const params = new URLSearchParams(window.location.search);
            const code = params.get('code');
            const state = params.get('state');
            const error = params.get('error');
            const errorDescription = params.get('error_description');
            const callbackKey = 'jupyter_ai_auth0_callback';

            const payload = {
                type: 'auth0_callback',
                code: code,
                state: state,
                error: errorDescription || error || undefined,
            };

            if (window.opener) {
                window.opener.postMessage(payload, window.location.origin);

                if (payload.error) {
                    document.getElementById('spinner').style.display = 'none';
                    document.getElementById('status').className = 'error';
                    document.getElementById('status').textContent = payload.error;
                    return;
                }

                document.getElementById('status').textContent = 'Sign in complete! You can close this window.';
                setTimeout(function() { window.close(); }, 1000);
            } else {
                // Fallback: store in localStorage for parent to pick up
                localStorage.setItem(callbackKey, JSON.stringify(payload));

                if (payload.error) {
                    document.getElementById('spinner').style.display = 'none';
                    document.getElementById('status').className = 'error';
                    document.getElementById('status').textContent = payload.error;
                    return;
                }

                document.getElementById('status').textContent = 'Sign in complete! Please return to JupyterLab.';
            }
        })();
    </script>
</body>
</html>
"""


# Global token store (initialized on first use)
_token_store: TokenStore | None = None
_token_store_config: tuple[str, str, str, str, str, bool] | None = None


def reset_token_store() -> None:
    """Reset the global token store (used when dev config changes)."""
    global _token_store, _token_store_config
    _token_store = None
    _token_store_config = None


def get_token_store(settings: dict | None = None) -> TokenStore:
    """Get or create the global token store.

    Args:
        settings: Jupyter server settings dict (used for initialization)
    """
    global _token_store, _token_store_config

    # Get config from settings if provided
    if settings:
        connector_settings = settings.get("jupyter_ai_connector", {})
        domain = connector_settings.get("auth0_domain", "")
        client_id = connector_settings.get("auth0_client_id", "")
        token_store_path = connector_settings.get("token_store_path", "")
        token_store_key = connector_settings.get("token_store_key", "")
        token_store_key_path = connector_settings.get("token_store_key_path", "")
        file_store_enabled = bool(connector_settings.get("token_store_file_enabled", True))
        config = (domain, client_id, token_store_path, token_store_key, token_store_key_path, file_store_enabled)

        # Reinitialize if config changed
        if _token_store is None or _token_store_config != config:
            _token_store = TokenStore(
                domain,
                client_id,
                file_store_path=token_store_path or None,
                file_store_key=token_store_key or None,
                file_store_key_path=token_store_key_path or None,
                file_store_enabled=file_store_enabled,
            )
            _token_store_config = config

    if _token_store is None:
        # Fallback - shouldn't happen in normal operation
        _token_store = TokenStore("", "")
        _token_store_config = ("", "", "", "", "", True)

    return _token_store


def decode_jwt_payload(token: str) -> dict[str, Any]:
    """Decode JWT payload without verification (for extracting claims)."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return {}

        payload = parts[1]
        # Add padding if needed
        padding = 4 - len(payload) % 4
        if padding != 4:
            payload += "=" * padding

        decoded = base64.urlsafe_b64decode(payload)
        return json.loads(decoded)
    except Exception as e:
        logger.warning(f"Failed to decode JWT: {e}")
        return {}


class OAuthCallbackHandler(APIHandler):
    """Handle OAuth callback from Auth0.

    Serves an HTML page that sends the authorization code back to the
    parent window via postMessage.
    """

    # Allow unauthenticated access (this is the OAuth callback)
    @property
    def login_handler(self):
        return None

    def set_default_headers(self):
        super().set_default_headers()
        # The callback page uses inline script/styles to postMessage the code.
        self.set_header("Content-Type", "text/html; charset=utf-8")
        self.set_header(
            "Content-Security-Policy",
            "default-src 'none'; frame-ancestors 'self'; "
            "script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'"
        )

    def check_xsrf_cookie(self):
        # Disable XSRF for OAuth callback (it's a redirect from Auth0)
        pass

    async def get(self):
        """Handle OAuth callback redirect from Auth0."""
        self.write(CALLBACK_HTML)
        self.finish(set_content_type="text/html")


class OAuthBaseHandler(APIHandler):
    """Base handler with Auth0 config helpers."""

    @property
    def auth0_config(self) -> dict:
        """Get Auth0 configuration from settings."""
        connector = self.settings.get("jupyter_ai_connector", {})
        return {
            "domain": connector.get("auth0_domain", ""),
            "client_id": connector.get("auth0_client_id", ""),
            "audience": connector.get("auth0_audience", ""),
        }

    @property
    def auth0_configured(self) -> bool:
        """Check if Auth0 is configured."""
        config = self.auth0_config
        return bool(config["domain"] and config["client_id"])


class OAuthConfigHandler(OAuthBaseHandler):
    """Provide OAuth configuration to the frontend."""

    async def get(self):
        """Return Auth0 configuration (public values only)."""
        if not self.auth0_configured:
            self.set_status(503)
            self.write({
                "error": "Auth0 not configured",
                "detail": "Auth0 domain and client_id must be configured"
            })
            self.finish()
            return

        config = self.auth0_config

        # Get the callback URL based on current request
        base_url = _get_public_origin(self.request)
        base_path = self.settings.get("base_url", "/")
        if not base_path.endswith("/"):
            base_path += "/"
        callback_url = f"{base_url}{base_path}ai/auth/callback"

        self.write({
            "domain": config["domain"],
            "clientId": config["client_id"],
            "audience": config["audience"],
            "callbackUrl": callback_url,
        })
        self.finish()


class OAuthExchangeHandler(OAuthBaseHandler):
    """Exchange authorization code for tokens."""

    async def post(self):
        """Exchange auth code + PKCE verifier for tokens."""
        if not self.auth0_configured:
            self.set_status(503)
            self.write({"error": "Auth0 not configured"})
            self.finish()
            return

        config = self.auth0_config

        try:
            body = json.loads(self.request.body)
            code = body.get("code")
            code_verifier = body.get("code_verifier")
            redirect_uri = body.get("redirect_uri")

            if not code or not code_verifier or not redirect_uri:
                self.set_status(400)
                self.write({"error": "Missing required fields: code, code_verifier, redirect_uri"})
                self.finish()
                return

            # Exchange code for tokens at Auth0
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"https://{config['domain']}/oauth/token",
                    data={
                        "grant_type": "authorization_code",
                        "client_id": config["client_id"],
                        "code": code,
                        "code_verifier": code_verifier,
                        "redirect_uri": redirect_uri,
                    },
                    headers={"Content-Type": "application/x-www-form-urlencoded"},
                )

                if response.status_code != 200:
                    logger.error(f"Token exchange failed: {response.text}")
                    try:
                        payload = response.json()
                        detail = payload.get("error_description") or payload.get("error") or response.text
                    except Exception:
                        detail = response.text
                    self.set_status(response.status_code)
                    self.write({
                        "error": "Token exchange failed",
                        "detail": detail,
                    })
                    self.finish()
                    return

                token_data = response.json()

            # Extract user info from ID token
            user_email = None
            user_name = None
            if "id_token" in token_data:
                claims = decode_jwt_payload(token_data["id_token"])
                user_email = claims.get("email")
                user_name = claims.get("name")

            # Get current Jupyter user ID
            user_id = self.current_user.username if self.current_user else "anonymous"

            # Store tokens
            store = get_token_store(self.settings)
            store.store_token(
                user_id=user_id,
                access_token=token_data["access_token"],
                expires_in=token_data.get("expires_in", 86400),
                refresh_token=token_data.get("refresh_token"),
                user_email=user_email,
                user_name=user_name,
            )

            logger.info(f"Stored Auth0 token for user {user_id}")

            self.write({
                "status": "ok",
                "user": {
                    "email": user_email,
                    "name": user_name,
                }
            })
            self.finish()

        except json.JSONDecodeError:
            self.set_status(400)
            self.write({"error": "Invalid JSON"})
            self.finish()
        except Exception as e:
            logger.exception("Token exchange error")
            self.set_status(500)
            self.write({"error": str(e)})
            self.finish()


class OAuthStatusHandler(OAuthBaseHandler):
    """Check authentication status."""

    async def get(self):
        """Return current authentication status."""
        user_id = self.current_user.username if self.current_user else "anonymous"
        store = get_token_store(self.settings)
        token = store.get_token(user_id)

        if token and token.is_expired():
            await store.refresh_token(user_id)
            token = store.get_token(user_id)

        storage = store.storage_backend

        if token and not token.is_expired():
            self.write({
                "authenticated": True,
                "user": {
                    "email": token.user_email,
                    "name": token.user_name,
                },
                "expiresAt": token.expires_at,
                "storage": storage,
            })
        else:
            self.write({
                "authenticated": False,
                "storage": storage,
            })
        self.finish()


class OAuthLogoutHandler(OAuthBaseHandler):
    """Handle logout - clear stored tokens."""

    async def post(self):
        """Clear stored tokens for current user."""
        user_id = self.current_user.username if self.current_user else "anonymous"
        store = get_token_store(self.settings)
        cleared = store.clear_token(user_id)

        logger.info(f"Cleared Auth0 token for user {user_id}")

        self.write({
            "status": "ok",
            "cleared": cleared,
        })
        self.finish()
