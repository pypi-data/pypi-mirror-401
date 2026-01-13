"""Tests for the synchronous FlowMyna client."""

import pytest
import respx
from httpx import Response
from uuid import UUID
from datetime import datetime, timezone

from flowmyna import FlowMyna
from flowmyna.exceptions import (
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError,
)


class TestClientInit:
    """Tests for FlowMyna client initialization."""

    def test_init_with_valid_key(self, api_key: str) -> None:
        """Test client initialization with valid API key."""
        client = FlowMyna(api_key=api_key)
        assert client is not None
        client.close()

    def test_init_without_key_raises_error(self) -> None:
        """Test that initialization without API key raises ValueError."""
        with pytest.raises(ValueError, match="api_key is required"):
            FlowMyna(api_key="")

    def test_init_with_invalid_prefix_raises_error(self) -> None:
        """Test that API key without correct prefix raises ValueError."""
        with pytest.raises(ValueError, match="must start with 'fm_live_'"):
            FlowMyna(api_key="invalid_key")

    def test_context_manager(self, api_key: str) -> None:
        """Test client as context manager."""
        with FlowMyna(api_key=api_key) as client:
            assert client is not None


class TestRecordEvent:
    """Tests for record_event method."""

    def test_record_event_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful event recording."""
        mock_api.post("/event").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "event_id": "12345678-1234-1234-1234-123456789abc",
                    "event_type": "Order Placed",
                    "timestamp": "2024-01-15T10:30:00Z",
                    "objects_count": 2,
                    "message": "Event 'Order Placed' recorded successfully",
                },
            )
        )

        with FlowMyna(api_key=api_key) as client:
            result = client.record_event(
                event="Order Placed",
                objects=[
                    {"type": "Order", "id": "ORD-123"},
                    {"type": "Customer", "id": "CUST-456"},
                ],
                properties={"total": 149.99},
            )

        assert result.success is True
        assert result.event_type == "Order Placed"
        assert result.objects_count == 2
        assert isinstance(result.event_id, UUID)

    def test_record_event_with_datetime_timestamp(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test event recording with datetime timestamp."""
        mock_api.post("/event").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "event_id": "12345678-1234-1234-1234-123456789abc",
                    "event_type": "Order Placed",
                    "timestamp": "2024-01-15T10:30:00+00:00",
                    "objects_count": 1,
                    "message": "Event recorded",
                },
            )
        )

        with FlowMyna(api_key=api_key) as client:
            result = client.record_event(
                event="Order Placed",
                objects=[{"type": "Order", "id": "ORD-123"}],
                timestamp=datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
            )

        assert result.success is True

    def test_record_event_authentication_error(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test authentication error handling."""
        mock_api.post("/event").mock(return_value=Response(401, json={"detail": "Invalid API key"}))

        with FlowMyna(api_key=api_key, max_retries=1) as client:
            with pytest.raises(AuthenticationError):
                client.record_event(
                    event="Order Placed",
                    objects=[{"type": "Order", "id": "ORD-123"}],
                )

    def test_record_event_validation_error(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test validation error handling."""
        mock_api.post("/event").mock(return_value=Response(422, json={"detail": "Event name is required"}))

        with FlowMyna(api_key=api_key, max_retries=1) as client:
            with pytest.raises(ValidationError):
                client.record_event(
                    event="",
                    objects=[{"type": "Order", "id": "ORD-123"}],
                )


class TestRecordEventBatch:
    """Tests for record_event_batch method."""

    def test_record_event_batch_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful batch event recording."""
        mock_api.post("/event/batch").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "processed": 3,
                    "failed": 0,
                    "event_ids": [
                        "11111111-1111-1111-1111-111111111111",
                        "22222222-2222-2222-2222-222222222222",
                        "33333333-3333-3333-3333-333333333333",
                    ],
                    "errors": None,
                },
            )
        )

        events = [
            {"event": "Case Opened", "objects": [{"type": "Case", "id": "CASE-001"}]},
            {"event": "Case Assigned", "objects": [{"type": "Case", "id": "CASE-001"}]},
            {"event": "Case Resolved", "objects": [{"type": "Case", "id": "CASE-001"}]},
        ]

        with FlowMyna(api_key=api_key) as client:
            result = client.record_event_batch(events)

        assert result.success is True
        assert result.processed == 3
        assert result.failed == 0
        assert len(result.event_ids) == 3

    def test_record_event_batch_exceeds_limit(self, api_key: str) -> None:
        """Test that batch exceeding 100 events raises error."""
        events = [{"event": f"Event {i}", "objects": [{"type": "Test", "id": f"T-{i}"}]} for i in range(101)]

        with FlowMyna(api_key=api_key) as client:
            with pytest.raises(ValidationError, match="Maximum 100 events"):
                client.record_event_batch(events)


class TestUpsertObject:
    """Tests for upsert_object method."""

    def test_upsert_object_create(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test creating a new object."""
        mock_api.post("/object/upsert").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "object_id": "12345678-1234-1234-1234-123456789abc",
                    "object_type": "Customer",
                    "external_id": "CUST-456",
                    "created": True,
                    "message": "Object 'Customer/CUST-456' created successfully",
                },
            )
        )

        with FlowMyna(api_key=api_key) as client:
            result = client.upsert_object(
                type="Customer",
                id="CUST-456",
                properties={"name": "Jane Doe", "tier": "gold"},
            )

        assert result.success is True
        assert result.created is True
        assert result.object_type == "Customer"
        assert result.external_id == "CUST-456"

    def test_upsert_object_update(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test updating an existing object."""
        mock_api.post("/object/upsert").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "object_id": "12345678-1234-1234-1234-123456789abc",
                    "object_type": "Customer",
                    "external_id": "CUST-456",
                    "created": False,
                    "message": "Object 'Customer/CUST-456' updated successfully",
                },
            )
        )

        with FlowMyna(api_key=api_key) as client:
            result = client.upsert_object(
                type="Customer",
                id="CUST-456",
                properties={"tier": "platinum"},
            )

        assert result.success is True
        assert result.created is False


class TestUpsertObjectBatch:
    """Tests for upsert_object_batch method."""

    def test_upsert_object_batch_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful batch object upsert."""
        mock_api.post("/object/batch").mock(
            return_value=Response(
                200,
                json={
                    "success": True,
                    "processed": 2,
                    "failed": 0,
                    "objects": [
                        {
                            "object_id": "11111111-1111-1111-1111-111111111111",
                            "object_type": "Customer",
                            "external_id": "CUST-1",
                            "created": True,
                        },
                        {
                            "object_id": "22222222-2222-2222-2222-222222222222",
                            "object_type": "Customer",
                            "external_id": "CUST-2",
                            "created": True,
                        },
                    ],
                    "errors": None,
                },
            )
        )

        objects = [
            {"type": "Customer", "id": "CUST-1", "properties": {"tier": "gold"}},
            {"type": "Customer", "id": "CUST-2", "properties": {"tier": "silver"}},
        ]

        with FlowMyna(api_key=api_key) as client:
            result = client.upsert_object_batch(objects)

        assert result.success is True
        assert result.processed == 2
        assert len(result.objects) == 2

    def test_upsert_object_batch_exceeds_limit(self, api_key: str) -> None:
        """Test that batch exceeding 100 objects raises error."""
        objects = [{"type": "Test", "id": f"T-{i}"} for i in range(101)]

        with FlowMyna(api_key=api_key) as client:
            with pytest.raises(ValidationError, match="Maximum 100 objects"):
                client.upsert_object_batch(objects)


class TestHealth:
    """Tests for health method."""

    def test_health_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful health check."""
        mock_api.get("/health").mock(
            return_value=Response(
                200,
                json={
                    "status": "healthy",
                    "workspace_id": "12345678-1234-1234-1234-123456789abc",
                    "workspace_name": "My Workspace",
                    "dataset_id": "87654321-4321-4321-4321-cba987654321",
                    "dataset_name": "Production Data",
                    "api_key_name": "Production API Key",
                },
            )
        )

        with FlowMyna(api_key=api_key) as client:
            result = client.health()

        assert result.status == "healthy"
        assert result.workspace_name == "My Workspace"
        assert result.dataset_name == "Production Data"
        assert result.api_key_name == "Production API Key"


class TestRetryLogic:
    """Tests for retry logic."""

    def test_retry_on_server_error(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test that server errors trigger retries."""
        # First two calls fail, third succeeds
        mock_api.post("/event").mock(
            side_effect=[
                Response(500, json={"detail": "Internal server error"}),
                Response(500, json={"detail": "Internal server error"}),
                Response(
                    200,
                    json={
                        "success": True,
                        "event_id": "12345678-1234-1234-1234-123456789abc",
                        "event_type": "Test",
                        "timestamp": "2024-01-15T10:30:00Z",
                        "objects_count": 1,
                        "message": "Success",
                    },
                ),
            ]
        )

        with FlowMyna(api_key=api_key, max_retries=3) as client:
            result = client.record_event(
                event="Test",
                objects=[{"type": "Test", "id": "T-1"}],
            )

        assert result.success is True

    def test_rate_limit_error(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test rate limit error handling."""
        mock_api.post("/event").mock(
            return_value=Response(
                429,
                json={"detail": "Rate limit exceeded"},
                headers={"Retry-After": "60"},
            )
        )

        with FlowMyna(api_key=api_key, max_retries=1) as client:
            with pytest.raises(RateLimitError) as exc_info:
                client.record_event(
                    event="Test",
                    objects=[{"type": "Test", "id": "T-1"}],
                )

        assert exc_info.value.retry_after == 60
