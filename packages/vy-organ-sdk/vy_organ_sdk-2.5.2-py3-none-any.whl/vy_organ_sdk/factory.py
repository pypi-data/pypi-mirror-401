import os

from .client import OrganClient, ConfigError


async def create_client() -> OrganClient:
    zenoh_connect = os.environ.get("ZENOH_CONNECT")
    if zenoh_connect:
        endpoints = [e.strip() for e in zenoh_connect.split(",")]
        return await create_zenoh_client(endpoints)

    raise ConfigError(
        "No transport configured. Set ZENOH_CONNECT environment variable"
    )


async def create_zenoh_client(
    endpoints: list[str] | None = None,
    timeout_ms: int = 30000,
) -> OrganClient:
    try:
        from .zenoh_client import ZenohClient
    except ImportError:
        raise ConfigError("eclipse-zenoh is not installed. Install with: pip install eclipse-zenoh")

    return await ZenohClient.connect(endpoints, timeout_ms)
