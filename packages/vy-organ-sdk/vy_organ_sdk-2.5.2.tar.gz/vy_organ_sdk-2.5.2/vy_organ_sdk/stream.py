
import asyncio
from dataclasses import dataclass
from enum import Enum
from typing import Any, AsyncIterator, Callable, Optional, Union
import uuid
import time
import json

from .client import ClientError, TransportError, ConfigError


class StreamType(Enum):

    BIDIRECTIONAL = "bidirectional"
    SERVER_TO_CLIENT = "server_to_client"
    CLIENT_TO_SERVER = "client_to_server"


@dataclass
class StreamEndpoint:

    endpoint_type: str
    path: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    address: Optional[str] = None

    @classmethod
    def unix_socket(cls, path: str) -> "StreamEndpoint":
        return cls(endpoint_type="unix_socket", path=path)

    @classmethod
    def zenoh(cls, address: str) -> "StreamEndpoint":
        return cls(endpoint_type="zenoh", address=address)

    @classmethod
    def cns_bus(cls, address: str) -> "StreamEndpoint":
        return cls(endpoint_type="cns_bus", address=address)

    def to_uri(self) -> str:
        if self.endpoint_type == "unix_socket":
            return f"unix://{self.path}"
        elif self.endpoint_type == "zenoh":
            return f"quic/{self.address}" if self.address else ""
        elif self.endpoint_type == "cns_bus":
            return self.address or ""
        return ""

    def to_dict(self) -> dict:
        result = {"type": self.endpoint_type}
        if self.path:
            result["path"] = self.path
        if self.host:
            result["host"] = self.host
        if self.port:
            result["port"] = self.port
        if self.address:
            result["address"] = self.address
        return result

    @classmethod
    def from_dict(cls, data: dict) -> "StreamEndpoint":
        return cls(
            endpoint_type=data.get("type", "unknown"),
            path=data.get("path"),
            host=data.get("host"),
            port=data.get("port"),
            address=data.get("address"),
        )


@dataclass
class StreamConnectRequest:

    target_organ: str
    target_intent: str
    stream_type: StreamType

    def to_dict(self) -> dict:
        return {
            "target_organ": self.target_organ,
            "target_intent": self.target_intent,
            "stream_type": self.stream_type.value,
        }


@dataclass
class StreamConnectResponse:

    stream_id: str
    endpoint: StreamEndpoint
    expires_in_secs: int

    @classmethod
    def from_dict(cls, data: dict) -> "StreamConnectResponse":
        return cls(
            stream_id=data["stream_id"],
            endpoint=StreamEndpoint.from_dict(data["endpoint"]),
            expires_in_secs=data.get("expires_in_secs", 300),
        )


STREAM_CONNECT_INTENT = "vy.stream.connect.v1"


StreamSender = asyncio.Queue
StreamReceiver = asyncio.Queue


class StreamContext:
 
    def __init__(
        self,
        stream_id: Optional[str] = None,
        buffer_size: int = 32,
    ):
        self.stream_id = stream_id or str(uuid.uuid4())
        self._send_queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=buffer_size)
        self._recv_queue: asyncio.Queue[Any] = asyncio.Queue(maxsize=buffer_size)
        self._closed = False
        self._error: Optional[Exception] = None

    @property
    def sender(self) -> asyncio.Queue:
        return self._send_queue

    @property
    def receiver(self) -> asyncio.Queue:
        return self._recv_queue

    async def send(self, data: Any) -> None:

        if self._closed:
            raise ClientError("Stream is closed")
        if self._error:
            raise self._error
        await self._send_queue.put(data)

    async def recv(self) -> Optional[Any]:

        if self._error:
            raise self._error
        if self._closed and self._recv_queue.empty():
            return None
        try:
            return await self._recv_queue.get()
        except asyncio.CancelledError:
            return None

    async def recv_nowait(self) -> Optional[Any]:

        try:
            return self._recv_queue.get_nowait()
        except asyncio.QueueEmpty:
            return None

    def close(self) -> None:
        self._closed = True

    def set_error(self, error: Exception) -> None:
        self._error = error
        self._closed = True

    @property
    def is_closed(self) -> bool:
        return self._closed

    async def __aiter__(self) -> AsyncIterator[Any]:
        while True:
            data = await self.recv()
            if data is None:
                break
            yield data


def create_stream_context(
    stream_id: Optional[str] = None,
    buffer_size: int = 32,
) -> StreamContext:

    return StreamContext(stream_id, buffer_size)


async def pipe_to_stream(
    source: AsyncIterator[Any],
    context: StreamContext,
) -> None:

    try:
        async for item in source:
            await context.send(item)
    finally:
        context.close()


async def collect_from_stream(
    context: StreamContext,
    max_items: Optional[int] = None,
) -> list:

    items = []
    count = 0
    async for item in context:
        items.append(item)
        count += 1
        if max_items and count >= max_items:
            break
    return items
