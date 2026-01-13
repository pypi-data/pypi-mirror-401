"""FlowMyna SDK Type Definitions.

This module defines dataclasses and type aliases used throughout the SDK.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID


# Type aliases for common structures
Properties = Dict[str, Any]


@dataclass
class EventObject:
    """An object (entity) associated with an event.

    Attributes:
        type: Object type name (e.g., "Order", "Customer")
        id: External ID of the object (e.g., "ORD-123")
        properties: Optional additional properties for the object
        qualifier: Optional role descriptor (e.g., "initiator", "target")
    """

    type: str
    id: str
    properties: Optional[Properties] = None
    qualifier: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        result: Dict[str, Any] = {"type": self.type, "id": self.id}
        if self.properties:
            result["properties"] = self.properties
        if self.qualifier:
            result["qualifier"] = self.qualifier
        return result


@dataclass
class EventResponse:
    """Response from recording a single event.

    Attributes:
        success: Whether the operation succeeded
        event_id: UUID of the created event
        event_type: Name of the event type
        timestamp: When the event occurred
        objects_count: Number of objects linked to the event
        message: Human-readable success message
    """

    success: bool
    event_id: UUID
    event_type: str
    timestamp: datetime
    objects_count: int
    message: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventResponse":
        """Create from API response dictionary."""
        return cls(
            success=data["success"],
            event_id=UUID(data["event_id"]),
            event_type=data["event_type"],
            timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            objects_count=data["objects_count"],
            message=data["message"],
        )


@dataclass
class EventBatchResponse:
    """Response from recording a batch of events.

    Attributes:
        success: True if all events were processed successfully
        processed: Number of events successfully processed
        failed: Number of events that failed
        event_ids: List of UUIDs for successfully created events
        errors: List of error messages for failed events (if any)
    """

    success: bool
    processed: int
    failed: int
    event_ids: List[UUID]
    errors: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EventBatchResponse":
        """Create from API response dictionary."""
        return cls(
            success=data["success"],
            processed=data["processed"],
            failed=data["failed"],
            event_ids=[UUID(eid) for eid in data["event_ids"]],
            errors=data.get("errors"),
        )


@dataclass
class ObjectUpsertResponse:
    """Response from upserting a single object.

    Attributes:
        success: Whether the operation succeeded
        object_id: UUID of the object
        object_type: Type of the object
        external_id: External ID of the object
        created: True if newly created, False if updated
        message: Human-readable success message
    """

    success: bool
    object_id: UUID
    object_type: str
    external_id: str
    created: bool
    message: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ObjectUpsertResponse":
        """Create from API response dictionary."""
        return cls(
            success=data["success"],
            object_id=UUID(data["object_id"]),
            object_type=data["object_type"],
            external_id=data["external_id"],
            created=data["created"],
            message=data["message"],
        )


@dataclass
class ObjectBatchItem:
    """Single item in an object batch response."""

    object_id: UUID
    object_type: str
    external_id: str
    created: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ObjectBatchItem":
        """Create from API response dictionary."""
        return cls(
            object_id=UUID(data["object_id"]),
            object_type=data["object_type"],
            external_id=data["external_id"],
            created=data["created"],
        )


@dataclass
class ObjectBatchResponse:
    """Response from upserting a batch of objects.

    Attributes:
        success: True if all objects were processed successfully
        processed: Number of objects successfully processed
        failed: Number of objects that failed
        objects: List of details for each processed object
        errors: List of error messages for failed objects (if any)
    """

    success: bool
    processed: int
    failed: int
    objects: List[ObjectBatchItem]
    errors: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ObjectBatchResponse":
        """Create from API response dictionary."""
        return cls(
            success=data["success"],
            processed=data["processed"],
            failed=data["failed"],
            objects=[ObjectBatchItem.from_dict(obj) for obj in data["objects"]],
            errors=data.get("errors"),
        )


@dataclass
class HealthResponse:
    """Response from health check endpoint.

    Attributes:
        status: Health status (e.g., "healthy")
        workspace_id: UUID of the workspace
        workspace_name: Name of the workspace
        dataset_id: UUID of the dataset linked to the API key
        dataset_name: Name of the dataset
        api_key_name: Name of the API key used
    """

    status: str
    workspace_id: UUID
    workspace_name: str
    dataset_id: UUID
    dataset_name: str
    api_key_name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HealthResponse":
        """Create from API response dictionary."""
        return cls(
            status=data["status"],
            workspace_id=UUID(data["workspace_id"]),
            workspace_name=data["workspace_name"],
            dataset_id=UUID(data["dataset_id"]),
            dataset_name=data["dataset_name"],
            api_key_name=data["api_key_name"],
        )


# Type for event input (can be dict or EventObject)
EventObjectInput = Dict[str, Any]


@dataclass
class EventInput:
    """Input structure for batch event recording."""

    event: str
    objects: List[EventObjectInput]
    timestamp: Optional[str] = None
    properties: Optional[Properties] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        result: Dict[str, Any] = {"event": self.event, "objects": self.objects}
        if self.timestamp:
            result["timestamp"] = self.timestamp
        if self.properties:
            result["properties"] = self.properties
        return result


@dataclass
class ObjectInput:
    """Input structure for batch object upsert."""

    type: str
    id: str
    properties: Optional[Properties] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API request."""
        result: Dict[str, Any] = {"type": self.type, "id": self.id}
        if self.properties:
            result["properties"] = self.properties
        return result
