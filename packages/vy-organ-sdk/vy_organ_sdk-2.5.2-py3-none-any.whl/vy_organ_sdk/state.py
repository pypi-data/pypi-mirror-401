from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional
import logging

from .codec import encode, decode

logger = logging.getLogger(__name__)


@dataclass
class StateValue:
    data: Any
    version: int = 1
    timestamp: datetime = field(default_factory=datetime.utcnow)
    ttl_ms: Optional[int] = None
    source: Optional[str] = None

    def with_ttl(self, ttl: timedelta) -> "StateValue":
        self.ttl_ms = int(ttl.total_seconds() * 1000)
        return self

    def with_source(self, source: str) -> "StateValue":
        self.source = source
        return self

    def with_version(self, version: int) -> "StateValue":
        self.version = version
        return self

    def is_expired(self) -> bool:
        if self.ttl_ms is None:
            return False
        elapsed = datetime.utcnow() - self.timestamp
        return elapsed.total_seconds() * 1000 > self.ttl_ms

    def to_dict(self) -> dict:
        return {
            "data": self.data,
            "version": self.version,
            "timestamp": int(self.timestamp.timestamp() * 1000),
            "ttl_ms": self.ttl_ms,
            "source": self.source,
        }

    def to_bytes(self) -> bytes:
        return encode(self.to_dict())

    @classmethod
    def from_dict(cls, d: dict) -> "StateValue":
        timestamp = datetime.utcfromtimestamp(d.get("timestamp", 0) / 1000)
        return cls(
            data=d.get("data"),
            version=d.get("version", 1),
            timestamp=timestamp,
            ttl_ms=d.get("ttl_ms"),
            source=d.get("source"),
        )

    @classmethod
    def from_bytes(cls, b: bytes) -> "StateValue":
        return cls.from_dict(decode(b))


@dataclass
class OrganStatus:
    organ_id: str
    version: str
    healthy: bool = True
    load: Optional[float] = None
    pending_requests: Optional[int] = None
    last_request_at: Optional[datetime] = None
    uptime_secs: Optional[int] = None
    intents: List[str] = field(default_factory=list)
    metadata: Optional[Dict[str, Any]] = None

    def with_intents(self, intents: List[str]) -> "OrganStatus":
        self.intents = intents
        return self

    def with_load(self, load: float) -> "OrganStatus":
        self.load = load
        return self

    def with_pending_requests(self, pending: int) -> "OrganStatus":
        self.pending_requests = pending
        return self

    def with_uptime(self, uptime_secs: int) -> "OrganStatus":
        self.uptime_secs = uptime_secs
        return self

    def unhealthy(self) -> "OrganStatus":
        self.healthy = False
        return self

    def to_dict(self) -> dict:
        result = {
            "organ_id": self.organ_id,
            "version": self.version,
            "healthy": self.healthy,
            "intents": self.intents,
        }
        if self.load is not None:
            result["load"] = self.load
        if self.pending_requests is not None:
            result["pending_requests"] = self.pending_requests
        if self.last_request_at is not None:
            result["last_request_at"] = self.last_request_at.isoformat()
        if self.uptime_secs is not None:
            result["uptime_secs"] = self.uptime_secs
        if self.metadata is not None:
            result["metadata"] = self.metadata
        return result

    @classmethod
    def from_dict(cls, d: dict) -> "OrganStatus":
        last_request_at = None
        if d.get("last_request_at"):
            last_request_at = datetime.fromisoformat(d["last_request_at"])
        return cls(
            organ_id=d["organ_id"],
            version=d.get("version", "0.0.0"),
            healthy=d.get("healthy", True),
            load=d.get("load"),
            pending_requests=d.get("pending_requests"),
            last_request_at=last_request_at,
            uptime_secs=d.get("uptime_secs"),
            intents=d.get("intents", []),
            metadata=d.get("metadata"),
        )


@dataclass
class StateDeclaration:
    key_pattern: str
    description: Optional[str] = None
    schema: Optional[dict] = None
    default_ttl: Optional[timedelta] = None
    queryable: bool = True

    def with_description(self, description: str) -> "StateDeclaration":
        self.description = description
        return self

    def with_schema(self, schema: dict) -> "StateDeclaration":
        self.schema = schema
        return self

    def with_ttl(self, ttl: timedelta) -> "StateDeclaration":
        self.default_ttl = ttl
        return self

    def not_queryable(self) -> "StateDeclaration":
        self.queryable = False
        return self


@dataclass
class StateUpdate:
    key: str
    value: StateValue
    operation: str = "put"


class StatePublisher:
    def __init__(self, session, organ_id: str, prefix: str = "agi"):
        self._session = session
        self._organ_id = organ_id
        self._prefix = prefix

    async def publish_state(self, key: str, value: StateValue) -> None:
        full_key = key if key.startswith(self._prefix) else f"{self._prefix}/{key}"
        payload = value.to_bytes()
        logger.debug(f"Publishing state: key={full_key}, version={value.version}")
        await self._session.put(full_key, payload)

    async def publish_organ_status(self, status: OrganStatus) -> None:
        key = f"{self._prefix}/organs/{status.organ_id}/status"
        value = StateValue(data=status.to_dict()).with_source(status.organ_id).with_ttl(timedelta(seconds=60))
        await self.publish_state(key, value)

    async def delete_state(self, key: str) -> None:
        full_key = key if key.startswith(self._prefix) else f"{self._prefix}/{key}"
        logger.debug(f"Deleting state: key={full_key}")
        await self._session.delete(full_key)


class StateSubscriber:
    def __init__(self, session, prefix: str = "agi"):
        self._session = session
        self._prefix = prefix

    async def get_state(self, key: str) -> Optional[StateValue]:
        full_key = key if key.startswith(self._prefix) else f"{self._prefix}/{key}"

        replies = await self._session.get(full_key)
        async for reply in replies:
            try:
                sample = reply.ok
                if sample:
                    value = StateValue.from_bytes(bytes(sample.payload))
                    if not value.is_expired():
                        return value
            except Exception as e:
                logger.warning(f"Failed to parse state reply: {e}")

        return None

    async def get_states_wildcard(self, pattern: str) -> List[tuple[str, StateValue]]:
        full_pattern = pattern if pattern.startswith(self._prefix) else f"{self._prefix}/{pattern}"

        logger.debug(f"Getting states with wildcard: pattern={full_pattern}")

        results = []
        replies = await self._session.get(full_pattern)
        async for reply in replies:
            try:
                sample = reply.ok
                if sample:
                    key = str(sample.key_expr)
                    value = StateValue.from_bytes(bytes(sample.payload))
                    if not value.is_expired():
                        results.append((key, value))
            except Exception as e:
                logger.warning(f"Failed to parse state reply: {e}")

        return results

    async def subscribe(self, pattern: str, callback: Callable[[StateUpdate], None]) -> None:
        full_pattern = pattern if pattern.startswith(self._prefix) else f"{self._prefix}/{pattern}"

        logger.info(f"Subscribing to state changes: pattern={full_pattern}")

        subscriber = await self._session.declare_subscriber(full_pattern)

        async def _process():
            async for sample in subscriber:
                try:
                    key = str(sample.key_expr)
                    value = StateValue.from_bytes(bytes(sample.payload))
                    update = StateUpdate(key=key, value=value, operation="put")
                    callback(update)
                except Exception as e:
                    logger.warning(f"Failed to process state update: {e}")

        import asyncio
        asyncio.create_task(_process())
