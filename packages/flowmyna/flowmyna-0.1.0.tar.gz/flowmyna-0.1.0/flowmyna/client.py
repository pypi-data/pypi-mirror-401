"""FlowMyna Synchronous Client.

This module provides the main synchronous client for interacting with the FlowMyna API.
"""

import time
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from .exceptions import (
    AuthenticationError,
    FlowMynaError,
    NetworkError,
    RateLimitError,
    ServerError,
    ValidationError,
)
from .types import (
    EventBatchResponse,
    EventResponse,
    HealthResponse,
    ObjectBatchResponse,
    ObjectUpsertResponse,
    Properties,
)

DEFAULT_BASE_URL = "https://api.flowmyna.com/api/public/v1"
DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RETRIES = 3


class FlowMyna:
    """Synchronous client for the FlowMyna API.

    This client provides methods to record process mining events and manage objects
    in FlowMyna. It uses httpx for HTTP requests and includes automatic retry logic.

    Args:
        api_key: Your FlowMyna API key (starts with 'fm_live_')
        base_url: API base URL (defaults to production)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum retry attempts for failed requests (default: 3)

    Example:
        >>> client = FlowMyna(api_key="fm_live_xxx")
        >>> client.record_event(
        ...     event="Order Placed",
        ...     objects=[{"type": "Order", "id": "ORD-123"}]
        ... )
    """

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
    ) -> None:
        if not api_key:
            raise ValueError("api_key is required")
        if not api_key.startswith("fm_live_"):
            raise ValueError("api_key must start with 'fm_live_'")

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout
        self._max_retries = max_retries

        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "flowmyna-python/0.1.0",
            },
            timeout=timeout,
        )

    def __enter__(self) -> "FlowMyna":
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle API response and raise appropriate exceptions."""
        if response.status_code == 200:
            return response.json()

        # Try to extract error message from response
        try:
            error_data = response.json()
            message = error_data.get("detail", str(error_data))
        except Exception:
            message = response.text or f"HTTP {response.status_code}"

        if response.status_code == 401:
            raise AuthenticationError(message)
        elif response.status_code == 422:
            raise ValidationError(message)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            raise RateLimitError(
                message,
                retry_after=int(retry_after) if retry_after else None,
            )
        elif response.status_code >= 500:
            raise ServerError(message, status_code=response.status_code)
        else:
            raise FlowMynaError(message, status_code=response.status_code)

    def _request_with_retry(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Make a request with automatic retry logic."""
        last_exception: Optional[Exception] = None

        for attempt in range(self._max_retries):
            try:
                response = self._client.request(method, path, json=json)
                return self._handle_response(response)

            except (RateLimitError, ServerError) as e:
                last_exception = e
                if attempt < self._max_retries - 1:
                    # Exponential backoff with jitter
                    wait_time = (2**attempt) + (time.time() % 1)
                    if isinstance(e, RateLimitError) and e.retry_after:
                        wait_time = e.retry_after
                    time.sleep(wait_time)
                else:
                    raise

            except httpx.TimeoutException as e:
                last_exception = NetworkError(f"Request timed out: {e}")
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
                else:
                    raise last_exception

            except httpx.RequestError as e:
                last_exception = NetworkError(f"Network error: {e}")
                if attempt < self._max_retries - 1:
                    time.sleep(2**attempt)
                else:
                    raise last_exception

        # Should not reach here, but just in case
        if last_exception:
            raise last_exception
        raise FlowMynaError("Request failed after retries")

    def record_event(
        self,
        event: str,
        objects: List[Dict[str, Any]],
        timestamp: Optional[Union[str, datetime]] = None,
        properties: Optional[Properties] = None,
    ) -> EventResponse:
        """Record a single process event.

        Args:
            event: Event name (1-200 characters)
            objects: List of objects involved in the event. Each object should have
                'type' and 'id' keys, and optionally 'properties' and 'qualifier'.
            timestamp: When the event occurred (ISO 8601 string or datetime).
                Defaults to current time.
            properties: Additional event properties/attributes.

        Returns:
            EventResponse with details of the created event.

        Raises:
            AuthenticationError: If the API key is invalid.
            ValidationError: If the request data is invalid.
            RateLimitError: If rate limit is exceeded.
            ServerError: If the server returns a 5xx error.

        Example:
            >>> client.record_event(
            ...     event="Order Placed",
            ...     objects=[
            ...         {"type": "Order", "id": "ORD-123"},
            ...         {"type": "Customer", "id": "CUST-456"}
            ...     ],
            ...     properties={"total": 149.99}
            ... )
        """
        payload: Dict[str, Any] = {"event": event, "objects": objects}

        if timestamp is not None:
            if isinstance(timestamp, datetime):
                payload["timestamp"] = timestamp.isoformat()
            else:
                payload["timestamp"] = timestamp

        if properties is not None:
            payload["properties"] = properties

        data = self._request_with_retry("POST", "/event", json=payload)
        return EventResponse.from_dict(data)

    def record_event_batch(
        self,
        events: List[Dict[str, Any]],
    ) -> EventBatchResponse:
        """Record multiple events in a single request.

        Args:
            events: List of event dictionaries. Each should have 'event' and 'objects'
                keys, and optionally 'timestamp' and 'properties'.
                Maximum 100 events per batch.

        Returns:
            EventBatchResponse with counts of processed/failed events.

        Example:
            >>> events = [
            ...     {"event": "Order Created", "objects": [{"type": "Order", "id": "ORD-1"}]},
            ...     {"event": "Order Shipped", "objects": [{"type": "Order", "id": "ORD-1"}]},
            ... ]
            >>> result = client.record_event_batch(events)
            >>> print(f"Processed: {result.processed}")
        """
        if len(events) > 100:
            raise ValidationError("Maximum 100 events per batch")

        payload = {"events": events}
        data = self._request_with_retry("POST", "/event/batch", json=payload)
        return EventBatchResponse.from_dict(data)

    def upsert_object(
        self,
        type: str,
        id: str,
        properties: Optional[Properties] = None,
    ) -> ObjectUpsertResponse:
        """Create or update an object.

        Uses upsert semantics: creates the object if it doesn't exist,
        or merges properties if it does.

        Args:
            type: Object type (1-100 characters), e.g., "Customer", "Order"
            id: External ID of the object (1-500 characters)
            properties: Object properties/attributes (merged with existing)

        Returns:
            ObjectUpsertResponse with details of the upserted object.

        Example:
            >>> result = client.upsert_object(
            ...     type="Customer",
            ...     id="CUST-456",
            ...     properties={"name": "Jane Doe", "tier": "gold"}
            ... )
            >>> print(f"Object {'created' if result.created else 'updated'}")
        """
        payload: Dict[str, Any] = {"type": type, "id": id}

        if properties is not None:
            payload["properties"] = properties

        data = self._request_with_retry("POST", "/object/upsert", json=payload)
        return ObjectUpsertResponse.from_dict(data)

    def upsert_object_batch(
        self,
        objects: List[Dict[str, Any]],
    ) -> ObjectBatchResponse:
        """Create or update multiple objects in a single request.

        Args:
            objects: List of object dictionaries. Each should have 'type' and 'id'
                keys, and optionally 'properties'. Maximum 100 objects per batch.

        Returns:
            ObjectBatchResponse with counts of processed/failed objects.

        Example:
            >>> objects = [
            ...     {"type": "Customer", "id": "CUST-1", "properties": {"tier": "gold"}},
            ...     {"type": "Customer", "id": "CUST-2", "properties": {"tier": "silver"}},
            ... ]
            >>> result = client.upsert_object_batch(objects)
            >>> print(f"Upserted {result.processed} objects")
        """
        if len(objects) > 100:
            raise ValidationError("Maximum 100 objects per batch")

        payload = {"objects": objects}
        data = self._request_with_retry("POST", "/object/batch", json=payload)
        return ObjectBatchResponse.from_dict(data)

    def health(self) -> HealthResponse:
        """Check API health and verify API key.

        Returns information about the workspace and dataset linked to the API key.

        Returns:
            HealthResponse with workspace and dataset details.

        Example:
            >>> health = client.health()
            >>> print(f"Connected to {health.workspace_name}")
            >>> print(f"Dataset: {health.dataset_name}")
        """
        data = self._request_with_retry("GET", "/health")
        return HealthResponse.from_dict(data)
