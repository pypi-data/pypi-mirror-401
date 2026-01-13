"""Tests for the asynchronous FlowMyna client."""

import pytest
import respx
from httpx import Response
from uuid import UUID
from datetime import datetime, timezone

from flowmyna import AsyncFlowMyna
from flowmyna.exceptions import (
    AuthenticationError,
    ValidationError,
)


class TestAsyncClientInit:
    """Tests for AsyncFlowMyna client initialization."""

    def test_init_with_valid_key(self, api_key: str) -> None:
        """Test client initialization with valid API key."""
        client = AsyncFlowMyna(api_key=api_key)
        assert client is not None

    def test_init_without_key_raises_error(self) -> None:
        """Test that initialization without API key raises ValueError."""
        with pytest.raises(ValueError, match="api_key is required"):
            AsyncFlowMyna(api_key="")

    def test_init_with_invalid_prefix_raises_error(self) -> None:
        """Test that API key without correct prefix raises ValueError."""
        with pytest.raises(ValueError, match="must start with 'fm_live_'"):
            AsyncFlowMyna(api_key="invalid_key")


class TestAsyncRecordEvent:
    """Tests for async record_event method."""

    @pytest.mark.asyncio
    async def test_record_event_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful async event recording."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.record_event(
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

    @pytest.mark.asyncio
    async def test_record_event_with_datetime_timestamp(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test async event recording with datetime timestamp."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.record_event(
                event="Order Placed",
                objects=[{"type": "Order", "id": "ORD-123"}],
                timestamp=datetime(2024, 1, 15, 10, 30, 0, tzinfo=timezone.utc),
            )

        assert result.success is True

    @pytest.mark.asyncio
    async def test_record_event_authentication_error(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test async authentication error handling."""
        mock_api.post("/event").mock(return_value=Response(401, json={"detail": "Invalid API key"}))

        async with AsyncFlowMyna(api_key=api_key, max_retries=1) as client:
            with pytest.raises(AuthenticationError):
                await client.record_event(
                    event="Order Placed",
                    objects=[{"type": "Order", "id": "ORD-123"}],
                )


class TestAsyncRecordEventBatch:
    """Tests for async record_event_batch method."""

    @pytest.mark.asyncio
    async def test_record_event_batch_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful async batch event recording."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.record_event_batch(events)

        assert result.success is True
        assert result.processed == 3
        assert result.failed == 0

    @pytest.mark.asyncio
    async def test_record_event_batch_exceeds_limit(self, api_key: str) -> None:
        """Test that async batch exceeding 100 events raises error."""
        events = [{"event": f"Event {i}", "objects": [{"type": "Test", "id": f"T-{i}"}]} for i in range(101)]

        async with AsyncFlowMyna(api_key=api_key) as client:
            with pytest.raises(ValidationError, match="Maximum 100 events"):
                await client.record_event_batch(events)


class TestAsyncUpsertObject:
    """Tests for async upsert_object method."""

    @pytest.mark.asyncio
    async def test_upsert_object_create(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test async creating a new object."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.upsert_object(
                type="Customer",
                id="CUST-456",
                properties={"name": "Jane Doe", "tier": "gold"},
            )

        assert result.success is True
        assert result.created is True
        assert result.object_type == "Customer"


class TestAsyncUpsertObjectBatch:
    """Tests for async upsert_object_batch method."""

    @pytest.mark.asyncio
    async def test_upsert_object_batch_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful async batch object upsert."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.upsert_object_batch(objects)

        assert result.success is True
        assert result.processed == 2


class TestAsyncHealth:
    """Tests for async health method."""

    @pytest.mark.asyncio
    async def test_health_success(self, api_key: str, mock_api: respx.MockRouter) -> None:
        """Test successful async health check."""
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

        async with AsyncFlowMyna(api_key=api_key) as client:
            result = await client.health()

        assert result.status == "healthy"
        assert result.workspace_name == "My Workspace"
