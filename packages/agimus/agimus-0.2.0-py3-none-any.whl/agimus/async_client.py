"""
Async Agimus Client - Async entry point for the SDK.

Uses httpx.AsyncClient for non-blocking HTTP requests.
"""
from typing import Any, Optional

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    AccessDeniedError,
    RateLimitError,
    ServerError,
)
from .async_query import AsyncQueryBuilder


# Default API base URL (can be overridden)
DEFAULT_BASE_URL = "https://api.agimus.ai"
DEFAULT_TIMEOUT = 30.0


class AsyncAgimusClient:
    """
    Async Agimus Platform SDK Client.

    Usage:
        async with AsyncAgimusClient(api_key="agm_...") as client:
            # Query objects
            customers = await client.objects("customer").filter(status="active").all()

            # Get single object
            customer = await client.objects("customer").get("C123")

            # CRUD operations
            await client.objects("customer").create({"id": "C1", "name": "Acme"})
            await client.objects("customer").update("C1", {"status": "premium"})
            await client.objects("customer").delete("C1")

    Or without context manager:
        client = AsyncAgimusClient(api_key="agm_...")
        try:
            customers = await client.objects("customer").all()
        finally:
            await client.close()
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: float = DEFAULT_TIMEOUT,
    ):
        """
        Initialize the async Agimus client.

        Args:
            api_key: API key (starts with "agm_")
            base_url: Override API base URL (default: https://api.agimus.ai)
            timeout: Request timeout in seconds (default: 30)

        Raises:
            ValueError: If api_key is missing or invalid format
        """
        if not api_key:
            raise ValueError("api_key is required")

        if not api_key.startswith("agm_"):
            raise ValueError("Invalid API key format. Keys should start with 'agm_'")

        self._api_key = api_key
        self._base_url = (base_url or DEFAULT_BASE_URL).rstrip("/")
        self._timeout = timeout

        # Create async HTTP client with default headers
        self._http = httpx.AsyncClient(
            base_url=f"{self._base_url}/api/v1/objects",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=timeout,
        )

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http.aclose()

    async def __aenter__(self) -> "AsyncAgimusClient":
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # =========================================================================
    # Public API - Query Builder
    # =========================================================================

    def objects(self, entity: str) -> AsyncQueryBuilder:
        """
        Start a query on an entity.

        Args:
            entity: Entity API name (e.g., "customer", "order")

        Returns:
            AsyncQueryBuilder for fluent query construction
        """
        return AsyncQueryBuilder(self, entity)

    # =========================================================================
    # Public API - Utility
    # =========================================================================

    async def health(self) -> dict:
        """
        Check API health.

        Returns:
            Health status with version info
        """
        return await self._request("GET", "/health")

    async def me(self) -> dict:
        """
        Get info about the current API key.

        Returns:
            API key info (tenantName, rateLimitPerMinute, requestId)
        """
        return await self._request("GET", "/me")

    # =========================================================================
    # Public API - Schema
    # =========================================================================

    async def list_entities(self) -> list[dict]:
        """
        List all accessible entities.

        Returns:
            List of entity summaries with apiName, displayName, pluralName,
            description, icon, iconColor
        """
        response = await self._request("GET", "/schema/entities")
        return response.get("entities", [])

    async def get_entity_schema(self, entity: str) -> dict:
        """
        Get full schema for an entity.

        Args:
            entity: Entity API name

        Returns:
            Entity schema with apiName, entityId, displayName, pluralName,
            description, primaryKey, properties, links
        """
        return await self._request("GET", f"/schema/entities/{entity}")

    async def get_properties(self, entity: str) -> list[dict]:
        """
        Get properties for an entity.

        Args:
            entity: Entity API name

        Returns:
            List of property schemas
        """
        response = await self._request("GET", f"/schema/entities/{entity}/properties")
        return response.get("properties", [])

    async def get_property(self, entity: str, property_name: str) -> dict:
        """
        Get details for a specific property.

        Args:
            entity: Entity API name
            property_name: Property API name

        Returns:
            Property schema with apiName, propertyId, displayName, description,
            baseType, isArray, nullable, isPrimaryKey, isEditable
        """
        response = await self._request("GET", f"/schema/entities/{entity}/properties/{property_name}")
        return response.get("property", {})

    async def get_primary_key(self, entity: str) -> dict:
        """
        Get primary key property for an entity.

        Args:
            entity: Entity API name

        Returns:
            Primary key property schema
        """
        response = await self._request("GET", f"/schema/entities/{entity}/primary-key")
        return response.get("primaryKey", {})

    async def get_links(self, entity: str) -> list[dict]:
        """
        Get links for an entity.

        Args:
            entity: Entity API name

        Returns:
            List of link schemas with apiName, displayName, targetEntity,
            cardinality, direction
        """
        response = await self._request("GET", f"/schema/entities/{entity}/links")
        return response.get("links", [])

    # =========================================================================
    # Internal Methods (called by AsyncQueryBuilder)
    # =========================================================================

    async def _query(self, entity: str, request: dict) -> dict:
        """Execute a query request."""
        return await self._request("POST", f"/{entity}/query", json=request)

    async def _get_object(
        self,
        entity: str,
        pk: str,
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
    ) -> dict:
        """Get single object by PK."""
        params = {}
        if fields:
            params["fields"] = ",".join(fields)
        if expand:
            params["expand"] = ",".join(expand)

        response = await self._request("GET", f"/{entity}/{pk}", params=params or None)
        return response.get("data", {})

    async def _batch_get(
        self,
        entity: str,
        pks: list[str],
        fields: Optional[list[str]] = None,
        expand: Optional[list[str]] = None,
    ) -> dict:
        """Get multiple objects by PKs."""
        request: dict[str, Any] = {"pks": pks}
        if fields:
            request["fields"] = fields
        if expand:
            request["expand"] = expand
        return await self._request("POST", f"/{entity}/batch-get", json=request)

    async def _count(self, entity: str, request: dict) -> int:
        """Get count of matching objects."""
        response = await self._request("POST", f"/{entity}/count", json=request)
        return response.get("count", 0)

    async def _distinct(
        self,
        entity: str,
        field: str,
        filter: Optional[dict] = None,
        limit: int = 1000,
    ) -> list[Any]:
        """Get distinct values for a field."""
        request: dict[str, Any] = {"field": field, "limit": limit}
        if filter:
            request["filter"] = filter
        response = await self._request("POST", f"/{entity}/distinct", json=request)
        return response.get("values", [])

    async def _aggregate(self, entity: str, request: dict) -> dict:
        """Run aggregation query."""
        return await self._request("POST", f"/{entity}/aggregate", json=request)

    async def _get_related(
        self,
        entity: str,
        pk: str,
        link: str,
        page_size: int = 50,
        offset: int = 0,
    ) -> dict:
        """Get related objects via link."""
        params = {"pageSize": page_size, "offset": offset}
        return await self._request("GET", f"/{entity}/{pk}/links/{link}", params=params)

    async def _count_related(self, entity: str, pk: str, link: str) -> int:
        """Count related objects via link."""
        response = await self._request("GET", f"/{entity}/{pk}/links/{link}/count")
        return response.get("count", 0)

    async def _create(self, entity: str, data: dict) -> dict:
        """Create an object."""
        response = await self._request("POST", f"/{entity}", json=data)
        return response.get("data", {})

    async def _update(self, entity: str, pk: str, data: dict) -> dict:
        """Update an object."""
        response = await self._request("PATCH", f"/{entity}/{pk}", json=data)
        return response.get("data", {})

    async def _upsert(self, entity: str, pk: str, data: dict) -> dict:
        """Upsert an object."""
        response = await self._request("PUT", f"/{entity}/{pk}", json=data)
        return response.get("data", {})

    async def _delete(self, entity: str, pk: str) -> bool:
        """Delete an object."""
        response = await self._request("DELETE", f"/{entity}/{pk}")
        return response.get("deleted", False)

    async def _batch(self, entity: str, operations: list[dict]) -> dict:
        """Execute batch operations."""
        return await self._request("POST", f"/{entity}/batch", json={"operations": operations})

    async def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json: Optional[dict] = None,
    ) -> dict:
        """
        Make an async HTTP request to the API.

        Args:
            method: HTTP method
            path: URL path (relative to base)
            params: Query parameters
            json: JSON body

        Returns:
            Response JSON

        Raises:
            APIError: On API error responses
        """
        try:
            response = await self._http.request(
                method=method,
                url=path,
                params=params,
                json=json,
            )
        except httpx.TimeoutException:
            raise ServerError("Request timed out", status_code=504)
        except httpx.ConnectError:
            raise ServerError("Failed to connect to API", status_code=503)

        return self._handle_response(response)

    def _handle_response(self, response: httpx.Response) -> dict:
        """
        Handle API response and raise appropriate exceptions.

        Args:
            response: HTTP response

        Returns:
            Response JSON data

        Raises:
            Various exceptions based on status code
        """
        # Success
        if response.status_code < 400:
            if response.status_code == 204:
                return {}
            return response.json()

        # Parse error response
        try:
            error_data = response.json()
            if "detail" in error_data:
                error = error_data["detail"].get("error", error_data["detail"])
            else:
                error = error_data.get("error", error_data)

            code = error.get("code", "UNKNOWN_ERROR") if isinstance(error, dict) else "UNKNOWN_ERROR"
            message = error.get("message", "An error occurred") if isinstance(error, dict) else str(error)
            request_id = error.get("requestId") if isinstance(error, dict) else None
            field = error.get("field") if isinstance(error, dict) else None
        except Exception:
            code = "UNKNOWN_ERROR"
            message = response.text or "An error occurred"
            request_id = None
            field = None

        status = response.status_code

        if status == 401:
            raise AuthenticationError(message)

        if status == 403:
            raise AccessDeniedError(message)

        if status == 404:
            raise NotFoundError(entity=code, pk=None)

        if status == 409:
            raise ValidationError(message, field=field, details={"code": code})

        if status == 422 or status == 400:
            raise ValidationError(message, field=field, details={"code": code})

        if status == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(retry_after=int(retry_after) if retry_after else None)

        if status >= 500:
            raise ServerError(message, status_code=status)

        raise APIError(
            code=code,
            message=message,
            status_code=status,
            request_id=request_id,
            field=field,
        )
