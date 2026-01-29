import json
import logging
import os
from pathlib import Path

from .handler import OrganHandler

log_level = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def launch_organ(
    handler: OrganHandler,
    manifest_path: str = "manifest.json",
    validate: bool = True,
    strict_validation: bool = True,
):
    manifest_file = Path(manifest_path)
    if not manifest_file.exists():
        raise FileNotFoundError(f"Manifest not found: {manifest_path}")

    with open(manifest_file) as f:
        manifest = json.load(f)

    if validate:
        from .validation import validate_handler_against_manifest, ValidationError
        try:
            validate_handler_against_manifest(
                handler.supported_intents,
                manifest_path,
                strict=strict_validation
            )
        except ValidationError as e:
            if strict_validation:
                raise ValueError(f"Manifest validation failed: {e}")
            else:
                logger.warning(f"Validation error (continuing): {e}")

    transport_config = manifest.get("transport", {})

    logger.info("Launching organ with Zenoh transport")
    logger.info(f"Supported intents: {handler.supported_intents}")

    try:
        from .transports.zenoh_server import ZenohOrganServer
    except ImportError as e:
        logger.error("Zenoh transport requires eclipse-zenoh: pip install eclipse-zenoh")
        raise ValueError(f"Zenoh transport not available: {e}")

    zenoh_config = transport_config.get("zenoh", {})
    connect = zenoh_config.get("connect", ["tcp/localhost:7447"])
    organ_id = manifest.get("organ_id", manifest.get("id", manifest.get("name")))

    import asyncio
    server = ZenohOrganServer(handler, connect=connect, organ_id=organ_id)
    asyncio.run(server.start())
