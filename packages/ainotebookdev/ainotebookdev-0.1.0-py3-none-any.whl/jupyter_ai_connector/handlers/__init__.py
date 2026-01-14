"""HTTP Handlers for Jupyter AI Connector."""

from .sessions import SessionHandler, SessionHistoryHandler, SessionInfoHandler
from .notebooks import NotebookResolveHandler, NotebookThreadHandler, NotebookThreadsHandler
from .events import SSEProxyHandler
from .commands import CommandProxyHandler
from .config import ConfigProxyHandler
from .oauth import (
    OAuthCallbackHandler,
    OAuthConfigHandler,
    OAuthExchangeHandler,
    OAuthStatusHandler,
    OAuthLogoutHandler,
)
from .dev_config import DevConfigHandler, DevConfigUiHandler


def setup_handlers(web_app, settings):
    """Set up the handlers for the connector."""
    host_pattern = ".*$"
    base_url = web_app.settings.get("base_url", "/")

    handlers = [
        # OAuth authentication
        (f"{base_url}ai/auth/callback", OAuthCallbackHandler),
        (f"{base_url}ai/auth/config", OAuthConfigHandler),
        (f"{base_url}ai/auth/exchange", OAuthExchangeHandler),
        (f"{base_url}ai/auth/status", OAuthStatusHandler),
        (f"{base_url}ai/auth/logout", OAuthLogoutHandler),
        # Session management
        (f"{base_url}ai/sessions", SessionHandler),
        # Notebook thread resolution + management
        (f"{base_url}ai/notebooks/([^/]+)/resolve", NotebookResolveHandler),
        (f"{base_url}ai/notebooks/([^/]+)/threads", NotebookThreadsHandler),
        (f"{base_url}ai/notebooks/([^/]+)/threads/([^/]+)", NotebookThreadHandler),
        # SSE event stream
        (f"{base_url}ai/sessions/([^/]+)/events", SSEProxyHandler),
        # Session history
        (f"{base_url}ai/sessions/([^/]+)/history", SessionHistoryHandler),
        # Command ingress
        (f"{base_url}ai/sessions/([^/]+)/commands", CommandProxyHandler),
        # Session info
        (f"{base_url}ai/sessions/([^/]+)", SessionInfoHandler),
        # Config proxy
        (f"{base_url}ai/config/(.*)", ConfigProxyHandler),
    ]

    if settings.get("jupyter_ai_connector_dev", {}).get("enabled"):
        handlers.extend([
            (f"{base_url}ai/dev/config", DevConfigHandler),
            (f"{base_url}ai/dev", DevConfigUiHandler),
        ])

    web_app.add_handlers(host_pattern, handlers)
