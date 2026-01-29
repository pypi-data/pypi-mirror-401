"""
Codec module for wire protocol serialization.

Supports MessagePack (default) and JSON (for debugging).
"""
import os
from typing import Any, Dict, Union

try:
    import msgpack
    HAS_MSGPACK = True
except ImportError:
    HAS_MSGPACK = False


class CodecError(Exception):
    """Raised when encoding/decoding fails."""
    pass


class Codec:
    """Wire protocol codec for serialization."""

    MSGPACK = "msgpack"
    JSON = "json"

    def __init__(self, codec_type: str = None):
        if codec_type is None:
            codec_type = os.environ.get("VY_CODEC", self.MSGPACK).lower()

        if codec_type not in (self.MSGPACK, self.JSON):
            raise ValueError(f"Unknown codec: {codec_type}. Valid options: msgpack, json")

        self._codec_type = codec_type

        if codec_type == self.MSGPACK and not HAS_MSGPACK:
            raise ImportError(
                "msgpack is required for MessagePack codec. "
                "Install with: pip install msgpack"
            )

    @property
    def name(self) -> str:
        return self._codec_type

    @property
    def content_type(self) -> str:
        if self._codec_type == self.MSGPACK:
            return "application/msgpack"
        return "application/json"

    def encode(self, data: Union[Dict, Any]) -> bytes:
        """Encode data to bytes."""
        try:
            if self._codec_type == self.MSGPACK:
                return msgpack.packb(data, use_bin_type=True)
            else:
                import json
                return json.dumps(data).encode('utf-8')
        except Exception as e:
            raise CodecError(f"Failed to encode: {e}") from e

    def decode(self, data: bytes) -> Any:
        """Decode bytes to data."""
        try:
            if self._codec_type == self.MSGPACK:
                return msgpack.unpackb(data, raw=False)
            else:
                import json
                return json.loads(data.decode('utf-8'))
        except Exception as e:
            raise CodecError(f"Failed to decode: {e}") from e


_default_codec = None


def get_default_codec() -> Codec:
    """Get the default codec instance (lazy singleton)."""
    global _default_codec
    if _default_codec is None:
        _default_codec = Codec()
    return _default_codec


def encode(data: Union[Dict, Any]) -> bytes:
    """Encode data using the default codec."""
    return get_default_codec().encode(data)


def decode(data: bytes) -> Any:
    """Decode bytes using the default codec."""
    return get_default_codec().decode(data)
