"""Config proxy handler."""

import logging

from .base import BaseProxyHandler

logger = logging.getLogger(__name__)


class ConfigProxyHandler(BaseProxyHandler):
    """Proxy config requests to the orchestrator."""

    def _build_upstream_url(self, path: str) -> str:
        url = f"{self.orchestrator_url}/v1/config/{path}"
        query = self.request.query
        if query:
            url = f"{url}?{query}"
        return url

    async def get(self, path: str):
        """Get configuration.

        GET /ai/config/*
        """
        if not await self.ensure_upstream_auth():
            return
        try:
            response = await self.http_client.get(
                self._build_upstream_url(path),
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            self.write(response.content)
            self.finish()

        except Exception as e:
            logger.exception("Failed to get config")
            await self.handle_error(500, str(e), code="PROXY_ERROR")

    async def put(self, path: str):
        """Update configuration.

        PUT /ai/config/*
        """
        if not await self.ensure_upstream_auth():
            return
        try:
            body = self.request.body
            if len(body) > self.max_payload_size:
                await self.handle_error(413, "Payload too large", code="PAYLOAD_TOO_LARGE")
                return

            response = await self.http_client.put(
                self._build_upstream_url(path),
                content=body,
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            self.write(response.content)
            self.finish()

        except Exception as e:
            logger.exception("Failed to update config")
            await self.handle_error(500, str(e), code="PROXY_ERROR")

    async def post(self, path: str):
        """Create or confirm configuration.

        POST /ai/config/*
        """
        if not await self.ensure_upstream_auth():
            return
        try:
            body = self.request.body
            if len(body) > self.max_payload_size:
                await self.handle_error(413, "Payload too large", code="PAYLOAD_TOO_LARGE")
                return

            response = await self.http_client.post(
                self._build_upstream_url(path),
                content=body,
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            self.write(response.content)
            self.finish()

        except Exception as e:
            logger.exception("Failed to post config")
            await self.handle_error(500, str(e), code="PROXY_ERROR")

    async def delete(self, path: str):
        """Delete configuration.

        DELETE /ai/config/*
        """
        if not await self.ensure_upstream_auth():
            return
        try:
            response = await self.http_client.delete(
                self._build_upstream_url(path),
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            self.write(response.content)
            self.finish()

        except Exception as e:
            logger.exception("Failed to delete config")
            await self.handle_error(500, str(e), code="PROXY_ERROR")
