"""FlowMyna Python SDK.

Official Python SDK for FlowMyna - Process Mining Event Tracking.

Example:
    >>> from flowmyna import FlowMyna
    >>> client = FlowMyna(api_key="fm_live_xxx")
    >>> client.record_event(
    ...     event="Order Placed",
    ...     objects=[{"type": "Order", "id": "ORD-123"}]
    ... )

For async usage:
    >>> from flowmyna import AsyncFlowMyna
    >>> async with AsyncFlowMyna(api_key="fm_live_xxx") as client:
    ...     await client.record_event(
    ...         event="Order Placed",
    ...         objects=[{"type": "Order", "id": "ORD-123"}]
    ...     )
"""

__version__ = "0.1.0"

from .client import FlowMyna
from .async_client import AsyncFlowMyna
from .exceptions import (
    FlowMynaError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError,
    NetworkError,
)
from .types import (
    EventResponse,
    EventBatchResponse,
    ObjectUpsertResponse,
    ObjectBatchResponse,
    HealthResponse,
    EventObject,
)

__all__ = [
    # Version
    "__version__",
    # Clients
    "FlowMyna",
    "AsyncFlowMyna",
    # Exceptions
    "FlowMynaError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
    "ServerError",
    "NetworkError",
    # Response types
    "EventResponse",
    "EventBatchResponse",
    "ObjectUpsertResponse",
    "ObjectBatchResponse",
    "HealthResponse",
    "EventObject",
]
