import asyncio
import logging
import os
import sys
from typing import Any, List

import httpx
from llama_deploy.appserver.settings import ApiserverSettings
from llama_deploy.core.client.ssl_util import get_httpx_verify_param
from llama_deploy.core.deployment_config import DeploymentConfig
from workflows.server import AbstractWorkflowStore, HandlerQuery, PersistentHandler

from .keyed_lock import AsyncKeyedLock
from .lru_cache import LRUCache

if sys.version_info <= (3, 11):
    from typing_extensions import override
else:
    from typing import override

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "https://api.cloud.llamaindex.ai"


class AgentDataStore(AbstractWorkflowStore):
    """Workflow store backed by LlamaCloud Agent Data API using raw httpx."""

    def __init__(
        self, settings: DeploymentConfig, server_settings: ApiserverSettings
    ) -> None:
        agent_url_id: str | None = server_settings.cloud_persistence_name
        collection = "workflow_contexts"
        if agent_url_id is not None:
            parts = agent_url_id.split(":")
            if len(parts) > 1:
                collection = parts[1]
            agent_url_id = parts[0]
        else:
            agent_url_id = settings.name

        self.settings = settings
        self.collection = collection
        self.deployment_name = agent_url_id

        self.base_url = os.getenv("LLAMA_CLOUD_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
        self.api_key = os.getenv("LLAMA_CLOUD_API_KEY")
        self.project_id = os.getenv("LLAMA_DEPLOY_PROJECT_ID")

        self.lock = AsyncKeyedLock()
        # workflow id -> agent data id
        self.cache = LRUCache[str, str](maxsize=1024)

    def _get_headers(self) -> dict[str, str]:
        """Build HTTP headers for API requests."""
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if self.project_id:
            headers["Project-Id"] = self.project_id
        return headers

    def _get_client(self) -> httpx.AsyncClient:
        """Create a new httpx client."""
        return httpx.AsyncClient(
            headers=self._get_headers(),
            verify=get_httpx_verify_param(),
        )

    @override
    async def query(self, query: HandlerQuery) -> List[PersistentHandler]:
        filters = self._build_filters(query)
        search_request = {
            "deployment_name": self.deployment_name,
            "collection": self.collection,
            "filter": filters,
            "page_size": 1000,
        }
        async with self._get_client() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/beta/agent-data/:search",
                json=search_request,
            )
            response.raise_for_status()
            data = response.json()

        items = data.get("items", [])
        return [PersistentHandler(**item["data"]) for item in items]

    @override
    async def update(self, handler: PersistentHandler) -> None:
        async with self.lock.acquire(handler.handler_id):
            id = await self._get_item_id(handler)
            if id is None:
                item = await self._create_item(handler)
                item_id = item.get("id")
                if item_id is None:
                    raise ValueError(f"Failed to create handler {handler.handler_id}")
                self.cache.set(handler.handler_id, item_id)
            else:
                await self._update_item(id, handler)

    @override
    async def delete(self, query: HandlerQuery) -> int:
        filters = self._build_filters(query)
        search_request = {
            "deployment_name": self.deployment_name,
            "collection": self.collection,
            "filter": filters,
            "page_size": 1000,
        }
        async with self._get_client() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/beta/agent-data/:search",
                json=search_request,
            )
            response.raise_for_status()
            data = response.json()

        items = data.get("items", [])
        await asyncio.gather(
            *[self._delete_item(item["id"]) for item in items if item.get("id")]
        )
        return len(items)

    async def _create_item(self, handler: PersistentHandler) -> dict[str, Any]:
        """Create a new agent data item."""
        create_request = {
            "deployment_name": self.deployment_name,
            "collection": self.collection,
            "data": handler.model_dump(mode="json"),
        }
        async with self._get_client() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/beta/agent-data",
                json=create_request,
            )
            response.raise_for_status()
            return response.json()

    async def _update_item(self, item_id: str, handler: PersistentHandler) -> None:
        """Update an existing agent data item."""
        update_request = {
            "data": handler.model_dump(mode="json"),
        }
        async with self._get_client() as client:
            response = await client.put(
                f"{self.base_url}/api/v1/beta/agent-data/{item_id}",
                json=update_request,
            )
            response.raise_for_status()

    async def _delete_item(self, item_id: str) -> None:
        """Delete an agent data item."""
        async with self._get_client() as client:
            response = await client.delete(
                f"{self.base_url}/api/v1/beta/agent-data/{item_id}",
            )
            response.raise_for_status()

    async def _get_item_id(self, handler: PersistentHandler) -> str | None:
        cached_id = self.cache.get(handler.handler_id)
        if cached_id is not None:
            return cached_id
        search_filter = {"handler_id": {"eq": handler.handler_id}}
        search_request = {
            "deployment_name": self.deployment_name,
            "collection": self.collection,
            "filter": search_filter,
            "page_size": 1,
        }
        async with self._get_client() as client:
            response = await client.post(
                f"{self.base_url}/api/v1/beta/agent-data/:search",
                json=search_request,
            )
            response.raise_for_status()
            data = response.json()

        items = data.get("items", [])
        if not items:
            return None
        id = items[0].get("id")
        if id is None:
            return None
        self.cache.set(handler.handler_id, id)
        return id

    def _build_filters(self, query: HandlerQuery) -> dict[str, Any]:
        filters: dict[str, Any] = {}
        if query.handler_id_in is not None:
            filters["handler_id"] = {
                "includes": query.handler_id_in,
            }
        if query.workflow_name_in is not None:
            filters["workflow_name"] = {
                "includes": query.workflow_name_in,
            }
        if query.status_in is not None:
            filters["status"] = {
                "includes": query.status_in,
            }
        if query.is_idle is not None:
            if query.is_idle:
                # Filter for handlers where idle_since is set (any valid datetime)
                filters["idle_since"] = {
                    "gte": "1970-01-01T00:00:00Z",
                }
            else:
                # Filter for handlers where idle_since is not set (null)
                filters["idle_since"] = {
                    "eq": None,
                }
        return filters
