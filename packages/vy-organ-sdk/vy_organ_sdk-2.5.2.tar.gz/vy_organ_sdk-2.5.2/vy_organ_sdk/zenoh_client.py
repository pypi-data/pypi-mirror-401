import asyncio
import json
import logging
import os
from typing import Any, AsyncIterator, Optional

import zenoh

from .codec import encode, decode, CodecError
from .client import OrganClient, ClientRequest, TransportError, SerializationError
from .protocol import ProtocolResponse, Event
from .transports.zenoh_server import StreamChunk

logger = logging.getLogger(__name__)


class ZenohClient(OrganClient):

    def __init__(self, session: zenoh.Session, timeout_ms: int = 30000):
        self._session = session
        self._timeout_ms = timeout_ms

    @classmethod
    async def connect(
        cls,
        endpoints: list[str] | None = None,
        timeout_ms: int = 30000,
        cert_path: str | None = None,
        key_path: str | None = None,
        ca_path: str | None = None,
    ) -> "ZenohClient":
        if endpoints is None:
            endpoints = os.environ.get(
                "ZENOH_CONNECT", "localhost:7447"
            ).split(",")
            endpoints = [e.strip() for e in endpoints if e.strip()]

        quic_endpoints = [
            e if e.startswith("quic/") else f"quic/{e}"
            for e in endpoints
        ]

        timeout_ms_env = int(os.environ.get("ZENOH_TIMEOUT_MS", timeout_ms))
        timeout_ms = max(1000, min(timeout_ms_env, 3600000))
        cert_path = cert_path or os.environ.get("ZENOH_CERT_PATH")
        key_path = key_path or os.environ.get("ZENOH_KEY_PATH")
        ca_path = ca_path or os.environ.get("ZENOH_CA_PATH")

        config = zenoh.Config()
        config.insert_json5("connect/endpoints", json.dumps(quic_endpoints))
        config.insert_json5("mode", '"client"')

        if cert_path and key_path:
            config.insert_json5("transport/link/tls/connect_certificate", json.dumps(cert_path))
            config.insert_json5("transport/link/tls/connect_private_key", json.dumps(key_path))
            logger.info("TLS client certificate configured")

        if ca_path:
            config.insert_json5("transport/link/tls/root_ca_certificate", json.dumps(ca_path))
            logger.info("TLS CA certificate configured")

        session = await zenoh.open(config)
        logger.info(f"Connected to Zenoh via QUIC at {quic_endpoints}")

        return cls(session, timeout_ms)

    async def _send_request(self, request: ClientRequest) -> ProtocolResponse:
        proto_request = request.into_protocol_request()
        key_expr = proto_request.intent.replace(".", "/")

        try:
            payload = encode(proto_request.to_dict())
        except CodecError as e:
            raise SerializationError(f"Failed to serialize request: {e}")

        logger.debug(
            f"Sending Zenoh request: request_id={proto_request.request_id}, "
            f"intent={proto_request.intent}, key_expr={key_expr}"
        )

        timeout_secs = self._timeout_ms / 1000.0

        try:
            replies = await self._session.get(
                key_expr,
                payload=payload,
                timeout=timeout_secs,
            )

            reply = await replies.receive_async()
            if reply is None:
                raise TransportError("No reply received")

            if reply.ok is not None:
                response_bytes = bytes(reply.ok.payload)
            elif reply.err is not None:
                raise TransportError(f"Reply error: {bytes(reply.err.payload)}")
            else:
                raise TransportError("Invalid reply: no ok or err")

            response_data = decode(response_bytes)
            response = ProtocolResponse.from_dict(response_data)

            logger.debug(
                f"Received Zenoh response: request_id={proto_request.request_id}, ok={response.ok}"
            )

            return response

        except asyncio.TimeoutError:
            raise TransportError(f"Request timed out after {self._timeout_ms}ms")
        except CodecError as e:
            raise SerializationError(f"Failed to parse response: {e}")
        except Exception as e:
            raise TransportError(f"Zenoh request failed: {e}")

    async def invoke(self, intent: str, payload: Any) -> ProtocolResponse:
        request = ClientRequest(intent=intent, payload=payload)
        return await self._send_request(request)

    async def invoke_with_shadow(
        self, intent: str, payload: Any, shadow: bool
    ) -> ProtocolResponse:
        request = ClientRequest(intent=intent, payload=payload, shadow=shadow)
        return await self._send_request(request)

    async def invoke_idempotent(
        self, intent: str, payload: Any, idempotency_key: str
    ) -> ProtocolResponse:
        request = ClientRequest(
            intent=intent, payload=payload, idempotency_key=idempotency_key
        )
        return await self._send_request(request)

    async def invoke_stream(
        self, intent: str, payload: Any
    ) -> AsyncIterator[StreamChunk]:
        request = ClientRequest(intent=intent, payload=payload)
        proto_request = request.into_protocol_request()
        key_expr = proto_request.intent.replace(".", "/")

        try:
            payload_bytes = encode(proto_request.to_dict())
        except CodecError as e:
            raise SerializationError(f"Failed to serialize request: {e}")

        logger.debug(
            f"Starting Zenoh stream request: request_id={proto_request.request_id}, "
            f"intent={proto_request.intent}, key_expr={key_expr}"
        )

        stream_timeout = 300.0

        try:
            replies = await self._session.get(
                key_expr,
                payload=payload_bytes,
                timeout=stream_timeout,
                consolidation=zenoh.ConsolidationMode.NONE,
            )

            while True:
                reply = await replies.receive_async()
                if reply is None:
                    break

                try:
                    if reply.ok is not None:
                        chunk_bytes = bytes(reply.ok.payload)
                    elif reply.err is not None:
                        raise TransportError(f"Stream reply error: {bytes(reply.err.payload)}")
                    else:
                        continue

                    chunk_data = decode(chunk_bytes)
                    chunk = StreamChunk.from_dict(chunk_data)

                    yield chunk

                    if chunk.final_chunk:
                        break

                except CodecError as e:
                    raise SerializationError(f"Failed to parse stream chunk: {e}")

        except asyncio.TimeoutError:
            raise TransportError(f"Stream timed out after {stream_timeout}s")
        except Exception as e:
            if "SerializationError" not in str(type(e)):
                raise TransportError(f"Zenoh stream failed: {e}")
            raise

    async def emit(self, subject: str, payload: Any) -> None:
        event = Event.new("custom", payload).with_subject(subject)
        key_expr = subject.replace(".", "/")

        try:
            event_bytes = encode(event.to_dict())
        except CodecError as e:
            raise SerializationError(f"Failed to serialize event: {e}")

        await self._session.put(key_expr, event_bytes)
        logger.debug(f"Emitted event via Zenoh: subject={subject}")

    async def emit_with_trace(
        self, subject: str, payload: Any, trace_id: str
    ) -> None:
        event = Event.new("custom", payload).with_subject(subject).with_trace_id(trace_id)
        key_expr = subject.replace(".", "/")

        try:
            event_bytes = encode(event.to_dict())
        except CodecError as e:
            raise SerializationError(f"Failed to serialize event: {e}")

        await self._session.put(key_expr, event_bytes)
        logger.debug(f"Emitted event with trace via Zenoh: subject={subject}, trace_id={trace_id}")

    def supports_pubsub(self) -> bool:
        return True

    async def close(self) -> None:
        await self._session.close()
        logger.info("Zenoh client closed")


async def create_zenoh_client(
    endpoints: list[str] | None = None,
    timeout_ms: int = 30000,
) -> ZenohClient:
    return await ZenohClient.connect(endpoints, timeout_ms)
