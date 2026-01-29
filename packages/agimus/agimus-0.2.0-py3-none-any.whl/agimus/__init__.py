"""
Agimus Python SDK.

A Python client for the Agimus Platform Object Store API.

Sync Usage:
    from agimus import AgimusClient

    client = AgimusClient(api_key="agm_...")

    # Query objects
    customers = client.objects("customer").filter(status="active").all()

    # Get single object
    customer = client.objects("customer").get("C123")

    # Create
    new_customer = client.objects("customer").create({"id": "C999", "name": "Acme"})

    # Update
    updated = client.objects("customer").update("C123", {"status": "premium"})

    # Delete
    client.objects("customer").delete("C123")

Async Usage:
    from agimus import AsyncAgimusClient

    async with AsyncAgimusClient(api_key="agm_...") as client:
        # Query objects
        customers = await client.objects("customer").filter(status="active").all()

        # Get single object
        customer = await client.objects("customer").get("C123")

        # Async iteration
        async for customer in client.objects("customer").filter(status="active"):
            print(customer["name"])
"""
from .client import AgimusClient
from .async_client import AsyncAgimusClient
from .exceptions import (
    AgimusError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    AccessDeniedError,
    RateLimitError,
    ServerError,
    APIError,
)

__version__ = "0.2.0"

__all__ = [
    "AgimusClient",
    "AsyncAgimusClient",
    "AgimusError",
    "AuthenticationError",
    "NotFoundError",
    "ValidationError",
    "AccessDeniedError",
    "RateLimitError",
    "ServerError",
    "APIError",
]
