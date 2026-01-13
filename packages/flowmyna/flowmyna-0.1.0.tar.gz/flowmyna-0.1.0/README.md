# FlowMyna Python SDK

Official Python SDK for [FlowMyna](https://flowmyna.com) - Process Mining Event Tracking.

## Installation

```bash
pip install flowmyna
```

Or with your preferred package manager:

```bash
uv add flowmyna
poetry add flowmyna
pipenv install flowmyna
```

For async support with HTTP/2:

```bash
pip install flowmyna[async]
```

## Quick Start

```python
from flowmyna import FlowMyna

# Initialize the client
client = FlowMyna(api_key="fm_live_your_key_here")

# Record an event
client.record_event(
    event="Order Placed",
    objects=[
        {"type": "Order", "id": "ORD-123"},
        {"type": "Customer", "id": "CUST-456"}
    ],
    properties={"total": 149.99}
)

# Upsert an object
client.upsert_object(
    type="Customer",
    id="CUST-456",
    properties={
        "name": "Jane Doe",
        "email": "jane@example.com"
    }
)
```

## Features

- **Simple API** - Intuitive methods for recording events and managing objects
- **Batch Operations** - Efficiently send up to 100 events/objects per request
- **Automatic Retries** - Built-in retry logic with exponential backoff
- **Type Hints** - Full type annotations for IDE support
- **Async Support** - Optional async client for high-concurrency applications

## Configuration

```python
import os
from flowmyna import FlowMyna

# Using environment variable (recommended)
client = FlowMyna(api_key=os.environ["FLOWMYNA_API_KEY"])

# With custom configuration
client = FlowMyna(
    api_key="fm_live_xxx",
    timeout=60,          # 60 second timeout
    max_retries=5,       # Retry up to 5 times
)
```

## Async Usage

```python
import asyncio
from flowmyna import AsyncFlowMyna

async def main():
    async with AsyncFlowMyna(api_key="fm_live_xxx") as client:
        await client.record_event(
            event="Order Placed",
            objects=[{"type": "Order", "id": "ORD-123"}]
        )

asyncio.run(main())
```

## Error Handling

```python
from flowmyna import FlowMyna
from flowmyna.exceptions import (
    FlowMynaError,
    AuthenticationError,
    ValidationError,
    RateLimitError,
    ServerError
)

client = FlowMyna(api_key="fm_live_xxx")

try:
    client.record_event(
        event="Order Placed",
        objects=[{"type": "Order", "id": "ORD-123"}]
    )
except AuthenticationError:
    print("Invalid API key")
except ValidationError as e:
    print(f"Invalid request: {e}")
except RateLimitError as e:
    print(f"Rate limited, retry after: {e.retry_after}")
except ServerError:
    print("Server error, please retry")
except FlowMynaError as e:
    print(f"Unexpected error: {e}")
```

## Documentation

Full documentation is available at [flowmyna.com/api/sdks/python](https://flowmyna.com/api/sdks/python)

## License

MIT License - see [LICENSE](LICENSE) for details.
