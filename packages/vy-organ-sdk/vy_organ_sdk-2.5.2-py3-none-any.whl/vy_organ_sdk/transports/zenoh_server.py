import asyncio
import json
import logging
import os
import signal
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Set

import zenoh

from ..codec import encode, decode, CodecError, get_default_codec
from ..handler import OrganHandler, HandlerRequest, HandlerResponse, StreamSender
from ..protocol import ProtocolRequest, ProtocolResponse, ProtocolError, StateEffect, LogEntry

logger = logging.getLogger(__name__)


@dataclass
class HealthResponse:
    healthy: bool
    version: str
    intents: list[str]
    streaming_intents: list[str]
    organ_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> dict:
        result = {
            "healthy": self.healthy,
            "version": self.version,
            "intents": self.intents,
            "streaming_intents": self.streaming_intents,
        }
        if self.organ_id:
            result["organ_id"] = self.organ_id
        if self.metadata:
            result["metadata"] = self.metadata
        return result


@dataclass
class StreamChunk:
    protocol_version: str
    chunk_type: str
    request_id: str
    sequence: int
    ok: bool
    data: Any
    error: Optional[ProtocolError] = None
    final_chunk: bool = False

    @classmethod
    def data_chunk(cls, request_id: str, sequence: int, data: Any) -> "StreamChunk":
        return cls(
            protocol_version="2",
            chunk_type="stream_chunk",
            request_id=request_id,
            sequence=sequence,
            ok=True,
            data=data,
            final_chunk=False,
        )

    @classmethod
    def end_chunk(cls, request_id: str, sequence: int) -> "StreamChunk":
        return cls(
            protocol_version="2",
            chunk_type="stream_end",
            request_id=request_id,
            sequence=sequence,
            ok=True,
            data=None,
            final_chunk=True,
        )

    @classmethod
    def error_chunk(cls, request_id: str, sequence: int, code: str, message: str) -> "StreamChunk":
        return cls(
            protocol_version="2",
            chunk_type="stream_error",
            request_id=request_id,
            sequence=sequence,
            ok=False,
            data=None,
            error=ProtocolError(code=code, message=message),
            final_chunk=True,
        )

    def to_dict(self) -> dict:
        result = {
            "protocol_version": self.protocol_version,
            "type": self.chunk_type,
            "request_id": self.request_id,
            "sequence": self.sequence,
            "ok": self.ok,
            "data": self.data,
            "final_chunk": self.final_chunk,
        }
        if self.error:
            result["error"] = self.error.to_dict()
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "StreamChunk":
        error = None
        if data.get("error"):
            error = ProtocolError(
                code=data["error"].get("code", "UNKNOWN"),
                message=data["error"].get("message", "Unknown error"),
            )
        return cls(
            protocol_version=data.get("protocol_version", "2"),
            chunk_type=data.get("type", "stream_chunk"),
            request_id=data.get("request_id", ""),
            sequence=data.get("sequence", 0),
            ok=data.get("ok", True),
            data=data.get("data"),
            error=error,
            final_chunk=data.get("final_chunk", False),
        )


class ZenohOrganServer:

    def __init__(
        self,
        handler: OrganHandler,
        connect: list[str] | None = None,
        max_concurrent: int = 100,
        organ_id: str | None = None,
        cert_path: str | None = None,
        key_path: str | None = None,
        ca_path: str | None = None,
    ):
        self.handler = handler
        connect_env = os.environ.get("ZENOH_CONNECT", "")
        if not connect and not connect_env:
            raise ValueError("ZENOH_CONNECT environment variable must be set")
        connect_str = connect or connect_env.split(",")
        self.connect = [e.strip() for e in connect_str if e.strip()]
        max_concurrent_env = int(os.environ.get("ZENOH_MAX_CONCURRENT", max_concurrent))
        self.max_concurrent = max(1, min(max_concurrent_env, 10000))
        self.organ_id = organ_id or os.environ.get("ORGAN_ID")
        self.cert_path = cert_path or os.environ.get("ZENOH_CERT_PATH")
        self.key_path = key_path or os.environ.get("ZENOH_KEY_PATH")
        self.ca_path = ca_path or os.environ.get("ZENOH_CA_PATH")

        self.supported_intents: Set[str] = set(handler.supported_intents)
        self.streaming_intents: Set[str] = set(handler.streaming_intents)

        self._session: zenoh.Session | None = None
        self._active_requests: Set[str] = set()
        self._cancel_tokens: Dict[str, asyncio.Event] = {}
        self._semaphore: asyncio.Semaphore | None = None
        self._running = False

    def _quic_endpoints(self) -> list[str]:
        return [
            e if e.startswith("quic/") else f"quic/{e}"
            for e in self.connect
        ]

    async def start(self):
        quic_endpoints = self._quic_endpoints()

        config = zenoh.Config()
        config.insert_json5("connect/endpoints", json.dumps(quic_endpoints))
        config.insert_json5("mode", '"client"')

        if self.cert_path and self.key_path:
            config.insert_json5("transport/link/tls/connect_certificate", json.dumps(self.cert_path))
            config.insert_json5("transport/link/tls/connect_private_key", json.dumps(self.key_path))
            logger.info("TLS client certificate configured")

        if self.ca_path:
            config.insert_json5("transport/link/tls/root_ca_certificate", json.dumps(self.ca_path))
            logger.info("TLS CA certificate configured")

        self._session = zenoh.open(config)
        logger.info(f"Connected to Zenoh via QUIC at {quic_endpoints}")

        self._semaphore = asyncio.Semaphore(self.max_concurrent)
        self._running = True

        all_intents = list(self.supported_intents | self.streaming_intents)
        logger.info(
            f"Declaring {len(all_intents)} queryables "
            f"({len(self.supported_intents)} regular, {len(self.streaming_intents)} streaming)"
        )

        queryables = []
        for intent in all_intents:
            key_expr = intent.replace(".", "/")
            queryable = self._session.declare_queryable(key_expr)
            logger.info(f"Declared queryable: {key_expr}")
            queryables.append((intent, queryable))

        health_key = f"vy/health/{self.organ_id}" if self.organ_id else "vy/health/unknown"
        health_queryable = self._session.declare_queryable(health_key)
        logger.info(f"Declared health queryable: {health_key}")

        cancel_sub = self._session.declare_subscriber("vy/cancel/**")
        logger.info("Subscribed to cancellation key: vy/cancel/**")

        asyncio.create_task(self._handle_cancellations(cancel_sub))
        asyncio.create_task(self._handle_health(health_queryable))

        logger.info(
            f"Zenoh organ server ready (version: {self.handler.version}, max_concurrent: {self.max_concurrent})"
        )

        loop = asyncio.get_event_loop()
        shutdown_event = asyncio.Event()

        def handle_shutdown():
            logger.info("Received shutdown signal, stopping server...")
            self._running = False
            shutdown_event.set()

        for sig in (signal.SIGTERM, signal.SIGINT):
            loop.add_signal_handler(sig, handle_shutdown)

        async def handle_queryable(intent: str, queryable):
            is_streaming = intent in self.streaming_intents
            while self._running:
                try:
                    query = queryable.try_recv()
                    if query is not None:
                        asyncio.create_task(self._handle_query(query, is_streaming))
                    else:
                        await asyncio.sleep(0.01)
                except Exception as e:
                    if self._running:
                        logger.error(f"Queryable error for {intent}: {e}")
                    break

        tasks = []
        for intent, queryable in queryables:
            task = asyncio.create_task(handle_queryable(intent, queryable))
            tasks.append(task)

        try:
            await shutdown_event.wait()
        finally:
            logger.info("Shutting down Zenoh server...")
            self._running = False
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            self._session.close()
            logger.info("Zenoh server stopped")

    async def _handle_health(self, health_queryable):
        while self._running:
            try:
                query = health_queryable.try_recv()
                if query is not None:
                    response = HealthResponse(
                        healthy=self.handler.health(),
                        version=self.handler.version,
                        intents=list(self.supported_intents),
                        streaming_intents=list(self.streaming_intents),
                        organ_id=self.organ_id,
                    )
                    query.reply(query.key_expr, encode(response.to_dict()))
                else:
                    await asyncio.sleep(0.01)
            except Exception as e:
                if self._running:
                    logger.error(f"Health queryable error: {e}")
                break

    async def _handle_cancellations(self, subscriber):
        while self._running:
            try:
                sample = subscriber.try_recv()
                if sample is not None:
                    key = str(sample.key_expr)
                    if key.startswith("vy/cancel/"):
                        trace_id = key[len("vy/cancel/"):]
                        if trace_id in self._cancel_tokens:
                            logger.info(f"Cancelling request via vy/cancel: {trace_id}")
                            self._cancel_tokens[trace_id].set()
                else:
                    await asyncio.sleep(0.01)
            except Exception as e:
                logger.warning(f"Cancel subscriber error: {e}")
                break

    async def _handle_query(self, query, is_streaming: bool):
        async with self._semaphore:
            try:
                payload_bytes = query.payload
                if payload_bytes is None:
                    response = ProtocolResponse.failure("", "NO_PAYLOAD", "No payload in query")
                    query.reply(query.key_expr, encode(response.to_dict()))
                    return

                max_payload_size = int(os.environ.get("VY_MAX_PAYLOAD_SIZE", 10 * 1024 * 1024))
                if len(payload_bytes) > max_payload_size:
                    response = ProtocolResponse.failure("", "PAYLOAD_TOO_LARGE", f"Payload exceeds {max_payload_size} bytes")
                    query.reply(query.key_expr, encode(response.to_dict()))
                    return

                payload_data = decode(bytes(payload_bytes))
                proto_request = ProtocolRequest.from_dict(payload_data)

                request_id = proto_request.request_id
                trace_id = proto_request.trace.trace_id if proto_request.trace else ""

                if request_id in self._active_requests:
                    response = ProtocolResponse.error_retryable(
                        request_id, "DUPLICATE_REQUEST", "Request already being processed"
                    )
                    query.reply(query.key_expr, encode(response.to_dict()))
                    return

                self._active_requests.add(request_id)
                cancel_event = asyncio.Event()
                if trace_id:
                    self._cancel_tokens[trace_id] = cancel_event

                try:
                    if is_streaming:
                        await self._process_streaming_request(query, proto_request, cancel_event)
                    else:
                        response = await self._process_request(proto_request, cancel_event)
                        query.reply(query.key_expr, encode(response.to_dict()))
                finally:
                    self._active_requests.discard(request_id)
                    self._cancel_tokens.pop(trace_id, None)

            except Exception as e:
                logger.exception("Error processing query")
                response = ProtocolResponse.failure("", "INTERNAL_ERROR", "An internal error occurred")
                query.reply(query.key_expr, encode(response.to_dict()))

    async def _process_request(
        self,
        proto_request: ProtocolRequest,
        cancel_event: asyncio.Event,
    ) -> ProtocolResponse:
        handler_request = HandlerRequest(
            intent=proto_request.intent,
            payload=proto_request.payload or {},
            idempotency_key=proto_request.idempotency_key,
            request_id=proto_request.request_id,
            trace_id=proto_request.trace.trace_id if proto_request.trace else None,
            tenant_id=proto_request.context.tenant_id if proto_request.context else None,
            actor=proto_request.context.actor if proto_request.context else None,
            shadow=proto_request.context.shadow if proto_request.context else False,
            state=proto_request.state.data if proto_request.state else None,
            state_version=proto_request.state.version if proto_request.state else 0,
        )

        try:
            handler_task = asyncio.create_task(
                asyncio.to_thread(self.handler.handle, handler_request)
            )
            cancel_task = asyncio.create_task(cancel_event.wait())

            done, pending = await asyncio.wait(
                [handler_task, cancel_task],
                return_when=asyncio.FIRST_COMPLETED,
            )

            for task in pending:
                task.cancel()

            if cancel_task in done:
                return ProtocolResponse.failure(
                    proto_request.request_id, "CANCELLED", "Request was cancelled"
                )

            handler_resp: HandlerResponse = handler_task.result()

        except Exception as e:
            logger.exception(f"Handler error for {proto_request.intent}")
            return ProtocolResponse.failure(
                proto_request.request_id, "HANDLER_ERROR", "Handler execution failed"
            )

        state_effect = None
        if handler_resp.state_effect:
            state_version = proto_request.state.version if proto_request.state else 0
            state_effect = StateEffect(
                expected_state_version=state_version,
                patch=handler_resp.state_effect,
            )

        logs = []
        if handler_resp.logs:
            for log_entry in handler_resp.logs:
                logs.append(LogEntry(
                    ts=log_entry.get("ts", time.time()),
                    level=log_entry.get("level", "info"),
                    event=log_entry.get("event", log_entry.get("message", "")),
                    data=log_entry.get("data"),
                ))

        error = None
        if not handler_resp.ok:
            error = ProtocolError(
                code=handler_resp.error_code or "UNKNOWN",
                message=handler_resp.error_message or "Unknown error",
            )

        return ProtocolResponse(
            request_id=proto_request.request_id,
            ok=handler_resp.ok,
            result=handler_resp.result,
            error=error,
            state_effect=state_effect,
            logs=logs,
        )

    async def _process_streaming_request(
        self,
        query,
        proto_request: ProtocolRequest,
        cancel_event: asyncio.Event,
    ) -> None:
        request_id = proto_request.request_id

        handler_request = HandlerRequest(
            intent=proto_request.intent,
            payload=proto_request.payload or {},
            idempotency_key=proto_request.idempotency_key,
            request_id=proto_request.request_id,
            trace_id=proto_request.trace.trace_id if proto_request.trace else None,
            tenant_id=proto_request.context.tenant_id if proto_request.context else None,
            actor=proto_request.context.actor if proto_request.context else None,
            shadow=proto_request.context.shadow if proto_request.context else False,
            state=proto_request.state.data if proto_request.state else None,
            state_version=proto_request.state.version if proto_request.state else 0,
        )

        sender: StreamSender = asyncio.Queue()
        sequence = 0
        cancelled = False

        try:
            stream_task = asyncio.create_task(
                self.handler.handle_stream(handler_request, sender)
            )
            cancel_task = asyncio.create_task(cancel_event.wait())

            while True:
                try:
                    chunk_data = await asyncio.wait_for(sender.get(), timeout=0.1)
                    chunk = StreamChunk.data_chunk(request_id, sequence, chunk_data)
                    query.reply(query.key_expr, encode(chunk.to_dict()))
                    logger.debug(f"Sent stream chunk: request_id={request_id}, sequence={sequence}")
                    sequence += 1
                except asyncio.TimeoutError:
                    if cancel_task.done():
                        cancelled = True
                        break
                    if stream_task.done():
                        while not sender.empty():
                            try:
                                chunk_data = sender.get_nowait()
                                chunk = StreamChunk.data_chunk(request_id, sequence, chunk_data)
                                query.reply(query.key_expr, encode(chunk.to_dict()))
                                logger.debug(f"Sent stream chunk: request_id={request_id}, sequence={sequence}")
                                sequence += 1
                            except asyncio.QueueEmpty:
                                break
                        break
                    continue

            for task in [stream_task, cancel_task]:
                if not task.done():
                    task.cancel()

            if cancelled:
                final_chunk = StreamChunk.error_chunk(request_id, sequence, "CANCELLED", "Stream was cancelled")
            elif stream_task.done() and stream_task.exception():
                error_msg = str(stream_task.exception())
                final_chunk = StreamChunk.error_chunk(request_id, sequence, "STREAM_ERROR", error_msg)
            else:
                final_chunk = StreamChunk.end_chunk(request_id, sequence)

            query.reply(query.key_expr, encode(final_chunk.to_dict()))
            logger.info(f"Stream completed: request_id={request_id}, chunks={sequence}")

        except Exception as e:
            logger.exception(f"Stream processor error: {e}")
            error_chunk = StreamChunk.error_chunk(request_id, sequence, "INTERNAL_ERROR", "Stream processing failed")
            query.reply(query.key_expr, encode(error_chunk.to_dict()))
