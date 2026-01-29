# VY Organ SDK (Python)

Python SDK for building VY-CNS organs with Protocol v2 support.

## Installation

```bash
pip install vy-organ-sdk
```

## Quick Start

```python
from vy_organ_sdk import OrganHandler, HandlerRequest, HandlerResponse
from vy_organ_sdk.transports import ZenohOrganServer

class MyOrgan(OrganHandler):
    version = "1.0.0"
    supported_intents = ["my.organ.hello.v1"]

    def handle(self, request: HandlerRequest) -> HandlerResponse:
        return HandlerResponse.success({"message": "Hello!"})

if __name__ == "__main__":
    import asyncio
    server = ZenohOrganServer(MyOrgan(), organ_id="my-organ")
    asyncio.run(server.start())
```

## Environment Variables

- `ZENOH_CONNECT` - Zenoh router endpoints (required)
- `ORGAN_ID` - Unique organ identifier
- `ZENOH_CERT_PATH` - TLS client certificate path
- `ZENOH_KEY_PATH` - TLS client key path
- `ZENOH_CA_PATH` - TLS CA certificate path

## License

MIT
