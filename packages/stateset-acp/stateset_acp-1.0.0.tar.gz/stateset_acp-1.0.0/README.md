# stateset-acp

Official Python client for the StateSet Agentic Commerce Protocol (ACP) Handler.

## Installation

```bash
pip install stateset-acp
```

## Quick Start

### HTTP Client

```python
import asyncio
from stateset_acp import AcpHttpClient

async def main():
    async with AcpHttpClient(
        base_url="http://localhost:8080",
        api_key="your_api_key",
    ) as client:
        # Create a checkout session
        session = await client.create_checkout_session(
            items=[{"id": "prod_123", "quantity": 1}],
        )

        # Update with customer info
        session = await client.update_checkout_session(
            session_id=session.id,
            customer={
                "billing_address": {
                    "name": "John Doe",
                    "email": "john@example.com",
                    "line1": "123 Main St",
                    "city": "San Francisco",
                    "region": "CA",
                    "postal_code": "94102",
                    "country": "US",
                },
            },
        )

        # Complete checkout
        result = await client.complete_checkout_session(
            session_id=session.id,
            payment={"delegated_token": "tok_xxx"},
        )

        print(f"Order ID: {result.order.id}")

asyncio.run(main())
```

### gRPC Client

```python
import asyncio
from stateset_acp import AcpGrpcClient

async def main():
    async with AcpGrpcClient(
        address="localhost:50051",
        api_key="your_api_key",
    ) as client:
        session = await client.create_checkout_session(
            items=[{"id": "prod_123", "quantity": 1}],
        )
        print(f"Session ID: {session.id}")

asyncio.run(main())
```

## API Reference

### AcpHttpClient

| Method | Description |
|--------|-------------|
| `create_checkout_session(items, customer?, fulfillment?)` | Create a new checkout session |
| `get_checkout_session(session_id)` | Get an existing session |
| `update_checkout_session(session_id, items?, customer?, fulfillment?)` | Update session details |
| `complete_checkout_session(session_id, payment, customer?, fulfillment?)` | Complete with payment |
| `cancel_checkout_session(session_id)` | Cancel a session |
| `delegate_payment(request)` | Create PSP vault token |
| `health_check()` | Check service health |

### AcpGrpcClient

| Method | Description |
|--------|-------------|
| `connect()` | Establish gRPC connection |
| `close()` | Close connection |
| `create_checkout_session(items, customer?, fulfillment?)` | Create a new checkout session |
| `get_checkout_session(session_id)` | Get an existing session |
| `update_checkout_session(session_id, items?, customer?, fulfillment?)` | Update session |
| `complete_checkout_session(session_id, payment, customer?, fulfillment?)` | Complete with payment |
| `cancel_checkout_session(session_id)` | Cancel a session |
| `delegate_payment(request)` | Create PSP vault token |

## Configuration

```python
from stateset_acp import AcpClientConfig

config = AcpClientConfig(
    base_url="http://localhost:8080",   # HTTP base URL
    grpc_address="localhost:50051",      # gRPC address
    api_key="your_api_key",              # API key for authentication
    timeout=30.0,                        # Request timeout in seconds
)
```

## Error Handling

```python
from stateset_acp import AcpHttpClient, AcpApiError

try:
    await client.create_checkout_session(items=[])
except AcpApiError as e:
    print(f"Type: {e.type}")
    print(f"Code: {e.code}")
    print(f"Message: {e}")
    print(f"Param: {e.param}")
    print(f"Status: {e.status_code}")
```

## Types

All Pydantic models are exported:

```python
from stateset_acp import (
    CheckoutSession,
    CheckoutSessionStatus,
    LineItem,
    Money,
    Customer,
    Address,
    Order,
    # ... and more
)
```

## Building gRPC Support

To use the gRPC client, you need to generate the protobuf files:

```bash
cd bindings/python
python -m grpc_tools.protoc \
    -I./stateset_acp/proto \
    --python_out=./stateset_acp/proto \
    --grpc_python_out=./stateset_acp/proto \
    ./stateset_acp/proto/acp_handler.proto
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black stateset_acp

# Type checking
mypy stateset_acp
```

## License

MIT
