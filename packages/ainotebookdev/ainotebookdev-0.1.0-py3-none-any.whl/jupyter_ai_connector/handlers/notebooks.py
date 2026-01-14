"""Notebook thread management handlers."""

import logging

from .base import BaseProxyHandler

logger = logging.getLogger(__name__)


class NotebookResolveHandler(BaseProxyHandler):
    """Proxy notebook thread resolution."""

    async def post(self, notebook_uuid: str):
        if not await self.ensure_upstream_auth():
            return

        try:
            body = self.request.body
            if len(body) > self.max_payload_size:
                await self.handle_error(413, "Payload too large", code="PAYLOAD_TOO_LARGE")
                return

            response = await self.http_client.post(
                f"{self.orchestrator_url}/v1/notebooks/{notebook_uuid}/resolve",
                content=body,
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ("content-encoding", "transfer-encoding", "content-length"):
                    self.set_header(key, value)

            self.write(response.content)
            self.finish()
        except Exception as e:
            logger.exception("Failed to resolve notebook thread")
            await self.handle_error(500, str(e), code="PROXY_ERROR")


class NotebookThreadsHandler(BaseProxyHandler):
    """Proxy notebook threads list and creation."""

    async def get(self, notebook_uuid: str):
        if not await self.ensure_upstream_auth():
            return

        try:
            response = await self.http_client.get(
                f"{self.orchestrator_url}/v1/notebooks/{notebook_uuid}/threads",
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ("content-encoding", "transfer-encoding", "content-length"):
                    self.set_header(key, value)

            self.write(response.content)
            self.finish()
        except Exception as e:
            logger.exception("Failed to list notebook threads")
            await self.handle_error(500, str(e), code="PROXY_ERROR")

    async def post(self, notebook_uuid: str):
        if not await self.ensure_upstream_auth():
            return

        try:
            body = self.request.body
            if len(body) > self.max_payload_size:
                await self.handle_error(413, "Payload too large", code="PAYLOAD_TOO_LARGE")
                return

            response = await self.http_client.post(
                f"{self.orchestrator_url}/v1/notebooks/{notebook_uuid}/threads",
                content=body,
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ("content-encoding", "transfer-encoding", "content-length"):
                    self.set_header(key, value)

            self.write(response.content)
            self.finish()
        except Exception as e:
            logger.exception("Failed to create notebook thread")
            await self.handle_error(500, str(e), code="PROXY_ERROR")


class NotebookThreadHandler(BaseProxyHandler):
    """Proxy notebook thread updates."""

    async def patch(self, notebook_uuid: str, session_id: str):
        if not await self.ensure_upstream_auth():
            return

        try:
            body = self.request.body
            if len(body) > self.max_payload_size:
                await self.handle_error(413, "Payload too large", code="PAYLOAD_TOO_LARGE")
                return

            response = await self.http_client.patch(
                f"{self.orchestrator_url}/v1/notebooks/{notebook_uuid}/threads/{session_id}",
                content=body,
                headers=await self.get_upstream_headers(),
            )

            self.set_status(response.status_code)
            for key, value in response.headers.items():
                if key.lower() not in ("content-encoding", "transfer-encoding", "content-length"):
                    self.set_header(key, value)

            self.write(response.content)
            self.finish()
        except Exception as e:
            logger.exception("Failed to update notebook thread")
            await self.handle_error(500, str(e), code="PROXY_ERROR")
