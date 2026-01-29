from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional
import uuid

from .protocol import (
    ProtocolRequest,
    ProtocolResponse,
    RequestTrace,
    RequestContext,
    RequestState,
    RequestCommit,
    Event,
)


class ClientError(Exception):
    pass


class TransportError(ClientError):
    def __init__(self, message: str):
        super().__init__(f"Transport error: {message}")
        self.message = message


class SerializationError(ClientError):
    def __init__(self, message: str):
        super().__init__(f"Serialization error: {message}")
        self.message = message


class RequestFailedError(ClientError):
    def __init__(self, message: str, code: Optional[str] = None, retryable: bool = False):
        super().__init__(f"Request failed: {message}")
        self.message = message
        self.code = code
        self.retryable = retryable


class TimeoutError(ClientError):
    def __init__(self, timeout_ms: int):
        super().__init__(f"Timeout after {timeout_ms}ms")
        self.timeout_ms = timeout_ms


class ConfigError(ClientError):
    def __init__(self, message: str):
        super().__init__(f"Configuration error: {message}")
        self.message = message


class PubSubError(ClientError):
    def __init__(self, message: str):
        super().__init__(f"Pub/sub error: {message}")
        self.message = message


class PubSubNotAvailableError(ClientError):
    def __init__(self):
        super().__init__("Pub/sub not available")


@dataclass
class ClientRequest:
    intent: str
    payload: Any
    idempotency_key: Optional[str] = None
    shadow: bool = False
    tenant_id: Optional[str] = None
    trace_id: Optional[str] = None

    def with_idempotency_key(self, key: str) -> "ClientRequest":
        self.idempotency_key = key
        return self

    def with_shadow(self, shadow: bool) -> "ClientRequest":
        self.shadow = shadow
        return self

    def with_tenant(self, tenant_id: str) -> "ClientRequest":
        self.tenant_id = tenant_id
        return self

    def with_trace(self, trace_id: str) -> "ClientRequest":
        self.trace_id = trace_id
        return self

    def into_protocol_request(self) -> ProtocolRequest:
        request_id = str(uuid.uuid4())
        idempotency_key = self.idempotency_key or str(uuid.uuid4())
        trace_id = self.trace_id or request_id

        return ProtocolRequest(
            protocol_version="2",
            request_type="request",
            request_id=request_id,
            intent=self.intent,
            idempotency_key=idempotency_key,
            payload=self.payload,
            trace=RequestTrace(
                trace_id=trace_id,
                span_id=str(uuid.uuid4()),
            ),
            context=RequestContext(
                tenant_id=self.tenant_id,
                shadow=self.shadow,
            ),
            state=RequestState(version=0, data=None),
            commit=RequestCommit(
                expected_state_version=0,
                allow_state_write=not self.shadow,
            ),
        )


class OrganClient(ABC):
    @abstractmethod
    async def invoke(self, intent: str, payload: Any) -> ProtocolResponse:
        pass

    @abstractmethod
    async def invoke_with_shadow(
        self, intent: str, payload: Any, shadow: bool
    ) -> ProtocolResponse:
        pass

    @abstractmethod
    async def invoke_idempotent(
        self, intent: str, payload: Any, idempotency_key: str
    ) -> ProtocolResponse:
        pass

    async def emit(self, subject: str, payload: Any) -> None:
        raise PubSubNotAvailableError()

    async def emit_with_trace(
        self, subject: str, payload: Any, trace_id: str
    ) -> None:
        raise PubSubNotAvailableError()

    def supports_pubsub(self) -> bool:
        return False

    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "OrganClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
