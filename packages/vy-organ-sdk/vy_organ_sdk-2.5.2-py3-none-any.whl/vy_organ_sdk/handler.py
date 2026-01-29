from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List, TYPE_CHECKING, Union
from dataclasses import dataclass, field
import asyncio

if TYPE_CHECKING:
    from .cancellation import CancellationToken
    from .stream import StreamContext

StreamSender = asyncio.Queue
StreamReceiver = asyncio.Queue


@dataclass
class HandlerRequest:

    intent: str

    payload: Dict[str, Any]

    idempotency_key: str

    request_id: str

    # Optional context fields
    tenant_id: Optional[str] = None

    actor: Optional[Dict[str, Any]] = None

    shadow: bool = False

    # Optional state fields
    state: Optional[Dict[str, Any]] = None

    state_version: int = 0

    # Cancellation support
    cancellation_token: Optional['CancellationToken'] = None

    trace_id: Optional[str] = None

    def check_cancelled(self) -> None:

        if self.cancellation_token:
            self.cancellation_token.check()

    @property
    def is_cancelled(self) -> bool:
        """Check if this request was cancelled.

        Returns:
            True if cancelled, False otherwise
        """
        if self.cancellation_token:
            return self.cancellation_token.is_cancelled
        return False


@dataclass
class HandlerResponse:
  
    ok: bool

    result: Optional[Dict[str, Any]] = None

    # Error fields (required if ok=False)
    error_code: Optional[str] = None

    error_message: Optional[str] = None

    # Optional fields
    state_effect: Optional[Dict[str, Any]] = None

    logs: Optional[List[Dict[str, Any]]] = field(default_factory=list)


class OrganHandler(ABC):
 
    @abstractmethod
    def handle(self, request: HandlerRequest) -> HandlerResponse:

        pass

    @property
    @abstractmethod
    def supported_intents(self) -> List[str]:

        pass

    @property
    def streaming_intents(self) -> List[str]:

        return []

    async def handle_stream(
        self,
        request: "HandlerRequest",
        sender: StreamSender,
    ) -> None:

        raise NotImplementedError("Streaming not implemented for this handler")

    def health(self) -> bool:

        return True

    @property
    def version(self) -> str:

        return "1.0.0"
