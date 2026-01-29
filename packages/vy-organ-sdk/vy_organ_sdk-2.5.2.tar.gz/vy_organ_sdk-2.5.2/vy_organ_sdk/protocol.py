from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import uuid
import time


@dataclass
class RequestTrace:
    trace_id: str = ""
    span_id: str = ""
    causation_id: Optional[str] = None
    correlation_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "trace_id": self.trace_id,
            "span_id": self.span_id,
        }
        if self.causation_id:
            result["causation_id"] = self.causation_id
        if self.correlation_id:
            result["correlation_id"] = self.correlation_id
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestTrace":
        return cls(
            trace_id=data.get("trace_id", ""),
            span_id=data.get("span_id", ""),
            causation_id=data.get("causation_id"),
            correlation_id=data.get("correlation_id"),
        )


@dataclass
class RequestContext:

    tenant_id: Optional[str] = None
    actor: Optional[Dict[str, Any]] = None
    shadow: bool = False

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {"shadow": self.shadow}
        if self.tenant_id:
            result["tenant_id"] = self.tenant_id
        if self.actor:
            result["actor"] = self.actor
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestContext":
        return cls(
            tenant_id=data.get("tenant_id"),
            actor=data.get("actor"),
            shadow=data.get("shadow", False),
        )


@dataclass
class RequestState:

    version: int = 0
    data: Any = None
    state_ref: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "version": self.version,
            "data": self.data if self.data is not None else None,
        }
        if self.state_ref:
            result["ref"] = self.state_ref
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestState":
        return cls(
            version=data.get("version", 0),
            data=data.get("data"),
            state_ref=data.get("ref"),
        )


@dataclass
class RequestCommit:

    expected_state_version: int = 0
    allow_state_write: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "expected_state_version": self.expected_state_version,
            "allow_state_write": self.allow_state_write,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RequestCommit":
        return cls(
            expected_state_version=data.get("expected_state_version", 0),
            allow_state_write=data.get("allow_state_write", True),
        )


@dataclass
class ProtocolRequest:

    protocol_version: str = "2"
    request_type: str = "request"
    request_id: str = ""
    intent: str = ""
    organ_target: Optional[str] = None
    idempotency_key: str = ""
    payload: Any = None
    trace: Optional[RequestTrace] = None
    context: Optional[RequestContext] = None
    state: Optional[RequestState] = None
    commit: Optional[RequestCommit] = None
    meta: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "protocol_version": self.protocol_version,
            "type": self.request_type,
            "request_id": self.request_id,
            "intent": self.intent,
            "idempotency_key": self.idempotency_key,
            "payload": self.payload if self.payload is not None else {},
        }
        if self.organ_target:
            result["organ_target"] = self.organ_target
        if self.trace:
            result["trace"] = self.trace.to_dict()
        if self.context:
            result["context"] = self.context.to_dict()
        if self.state:
            result["state"] = self.state.to_dict()
        if self.commit:
            result["commit"] = self.commit.to_dict()
        if self.meta:
            result["meta"] = self.meta
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProtocolRequest":
        return cls(
            protocol_version=data.get("protocol_version", "2"),
            request_type=data.get("type", "request"),
            request_id=data.get("request_id", ""),
            intent=data.get("intent", ""),
            organ_target=data.get("organ_target"),
            idempotency_key=data.get("idempotency_key", ""),
            payload=data.get("payload"),
            trace=RequestTrace.from_dict(data["trace"]) if data.get("trace") else None,
            context=RequestContext.from_dict(data["context"]) if data.get("context") else None,
            state=RequestState.from_dict(data["state"]) if data.get("state") else None,
            commit=RequestCommit.from_dict(data["commit"]) if data.get("commit") else None,
            meta=data.get("meta"),
        )


@dataclass
class ProtocolError:

    code: str
    message: str
    retryable: bool = False
    details: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "code": self.code,
            "message": self.message,
            "retryable": self.retryable,
        }
        if self.details is not None:
            result["details"] = self.details
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProtocolError":
        return cls(
            code=data.get("code", "UNKNOWN"),
            message=data.get("message", "Unknown error"),
            retryable=data.get("retryable", False),
            details=data.get("details"),
        )

    @classmethod
    def new(cls, code: str, message: str) -> "ProtocolError":
        return cls(code=code, message=message)

    def as_retryable(self) -> "ProtocolError":
        self.retryable = True
        return self

    def with_details(self, details: Any) -> "ProtocolError":
        self.details = details
        return self


@dataclass
class StateEffect:

    expected_state_version: int
    patch: Optional[Any] = None
    events: Optional[List["Event"]] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "expected_state_version": self.expected_state_version,
        }
        if self.patch is not None:
            result["patch"] = self.patch
        if self.events:
            result["events"] = [e.to_dict() for e in self.events]
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StateEffect":
        events = None
        if data.get("events"):
            events = [Event.from_dict(e) for e in data["events"]]
        return cls(
            expected_state_version=data.get("expected_state_version", 0),
            patch=data.get("patch"),
            events=events,
        )


@dataclass
class Event:

    event_type: str
    data: Any
    metadata: Optional[Any] = None

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    subject: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    trace_id: Optional[str] = None
    source: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "type": self.event_type,
            "data": self.data,
            "id": self.id,
            "subject": self.subject,
            "timestamp": self.timestamp,
        }
        if self.metadata is not None:
            result["metadata"] = self.metadata
        if self.trace_id:
            result["trace_id"] = self.trace_id
        if self.source:
            result["source"] = self.source
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Event":
        return cls(
            event_type=data.get("type", "unknown"),
            data=data.get("data"),
            metadata=data.get("metadata"),
            id=data.get("id", str(uuid.uuid4())),
            subject=data.get("subject", ""),
            timestamp=data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            trace_id=data.get("trace_id"),
            source=data.get("source"),
        )

    @classmethod
    def new(cls, event_type: str, payload: Any) -> "Event":
        return cls(event_type=event_type, data=payload)

    def with_subject(self, subject: str) -> "Event":
        self.subject = subject
        return self

    def with_trace_id(self, trace_id: str) -> "Event":
        self.trace_id = trace_id
        return self

    def with_source(self, source: str) -> "Event":
        self.source = source
        return self


@dataclass
class LogEntry:

    ts: float
    level: str
    event: str
    data: Optional[Any] = None

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "ts": self.ts,
            "level": self.level,
            "event": self.event,
        }
        if self.data is not None:
            result["data"] = self.data
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls(
            ts=data.get("ts", time.time()),
            level=data.get("level", "info"),
            event=data.get("event", ""),
            data=data.get("data"),
        )

    @classmethod
    def info(cls, message: str, data: Optional[Any] = None) -> "LogEntry":
        return cls(ts=time.time(), level="info", event=message, data=data)

    @classmethod
    def warn(cls, message: str, data: Optional[Any] = None) -> "LogEntry":
        return cls(ts=time.time(), level="warn", event=message, data=data)

    @classmethod
    def error(cls, message: str, data: Optional[Any] = None) -> "LogEntry":
        return cls(ts=time.time(), level="error", event=message, data=data)

    @classmethod
    def debug(cls, message: str, data: Optional[Any] = None) -> "LogEntry":
        return cls(ts=time.time(), level="debug", event=message, data=data)


@dataclass
class ProtocolResponse:
   
    protocol_version: str = "2"
    response_type: str = "response"
    request_id: str = ""
    ok: bool = True
    result: Any = None
    error: Optional[ProtocolError] = None
    state_effect: Optional[StateEffect] = None
    logs: List[LogEntry] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "protocol_version": self.protocol_version,
            "type": self.response_type,
            "request_id": self.request_id,
            "ok": self.ok,
            "result": self.result if self.result is not None else None,
        }
        if self.error:
            result["error"] = self.error.to_dict()
        if self.state_effect:
            result["state_effect"] = self.state_effect.to_dict()
        if self.logs:
            result["logs"] = [log.to_dict() for log in self.logs]
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ProtocolResponse":
        error = None
        if data.get("error"):
            error = ProtocolError.from_dict(data["error"])

        state_effect = None
        if data.get("state_effect"):
            state_effect = StateEffect.from_dict(data["state_effect"])

        logs = []
        if data.get("logs"):
            logs = [LogEntry.from_dict(log) for log in data["logs"]]

        return cls(
            protocol_version=data.get("protocol_version", "2"),
            response_type=data.get("type", "response"),
            request_id=data.get("request_id", ""),
            ok=data.get("ok", True),
            result=data.get("result"),
            error=error,
            state_effect=state_effect,
            logs=logs,
        )

    @classmethod
    def success(cls, request_id: str, result: Any) -> "ProtocolResponse":
        return cls(
            request_id=request_id,
            ok=True,
            result=result,
        )

    @classmethod
    def failure(cls, request_id: str, code: str, message: str) -> "ProtocolResponse":
        return cls(
            request_id=request_id,
            ok=False,
            error=ProtocolError(code=code, message=message),
        )

    @classmethod
    def error_retryable(cls, request_id: str, code: str, message: str) -> "ProtocolResponse":
        return cls(
            request_id=request_id,
            ok=False,
            error=ProtocolError(code=code, message=message, retryable=True),
        )

    def with_log(self, level: str, message: str, data: Optional[Any] = None) -> "ProtocolResponse":
        self.logs.append(LogEntry(ts=time.time(), level=level, event=message, data=data))
        return self

    def with_state_effect(self, patch: Any, version: int = 0) -> "ProtocolResponse":
        self.state_effect = StateEffect(expected_state_version=version, patch=patch)
        return self
