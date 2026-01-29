"""
Cancellation Token pattern for VY Organ SDK.

This module provides a clean, encapsulated API for handling request cancellation
in organs. The pattern is inspired by .NET's CancellationToken and Go's context.

Usage:
    from vy_organ_sdk import CancellationToken

    class MyOrgan(OrganHandler):
        async def handle(self, request: HandlerRequest) -> HandlerResponse:
            token = request.cancellation_token

            # Option 1: Check periodically
            for item in large_dataset:
                token.check()  # Raises CancelledError if cancelled
                await process(item)

            # Option 2: With timeout
            result = await token.with_timeout(
                self.long_operation(),
                timeout=30.0
            )

            # Option 3: Register cleanup
            token.on_cancel(lambda: self.cleanup_resources())

            # Option 4: Check without raising
            if token.is_cancelled:
                return HandlerResponse(ok=False, error_code="CANCELLED")
"""

import asyncio
import time
from typing import Callable, List, Optional, Any, Coroutine, TypeVar
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
from enum import Enum
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T')


class CancellationReason(Enum):
    """Reason for cancellation."""
    USER_REQUESTED = "user_requested"
    TIMEOUT = "timeout"
    SHUTDOWN = "shutdown"
    PARENT_CANCELLED = "parent_cancelled"
    UNKNOWN = "unknown"


@dataclass
class CancellationToken:
    """
    Token for cooperative cancellation of operations.

    This token is passed to handlers and can be used to:
    1. Check if cancellation was requested
    2. Raise exception if cancelled
    3. Register cleanup callbacks
    4. Create child tokens for sub-operations
    5. Wait with cancellation support

    The token is thread-safe and can be shared across async tasks.

    Example:
        async def handle(self, request: HandlerRequest) -> HandlerResponse:
            token = request.cancellation_token

            # Long operation with periodic checks
            for i in range(1000):
                token.check()  # Raises if cancelled
                await self.process_item(i)

            # Or use context manager
            async with token.scope():
                await self.risky_operation()
    """

    request_id: str = ""
    trace_id: str = ""
    reason: CancellationReason = CancellationReason.UNKNOWN

    _cancelled: bool = field(default=False, repr=False)
    _cancel_event: asyncio.Event = field(default_factory=asyncio.Event, repr=False)
    _callbacks: List[Callable[[], Any]] = field(default_factory=list, repr=False)
    _cancelled_at: Optional[float] = field(default=None, repr=False)
    _parent: Optional['CancellationToken'] = field(default=None, repr=False)

    def __post_init__(self):
        """Initialize event if not set."""
        if self._cancel_event is None:
            self._cancel_event = asyncio.Event()

    @property
    def is_cancelled(self) -> bool:
        """Check if cancellation was requested.

        Returns:
            True if cancelled, False otherwise
        """
        # Check parent first
        if self._parent and self._parent.is_cancelled:
            return True
        return self._cancelled

    @property
    def cancelled_at(self) -> Optional[float]:
        """Get timestamp when cancellation occurred.

        Returns:
            Unix timestamp or None if not cancelled
        """
        return self._cancelled_at

    def check(self) -> None:
        """Check if cancelled and raise if so.

        This is the primary method for cooperative cancellation.
        Call this periodically in long-running operations.

        Raises:
            asyncio.CancelledError: If cancellation was requested

        Example:
            for item in items:
                token.check()
                process(item)
        """
        if self.is_cancelled:
            raise asyncio.CancelledError(f"Request cancelled: {self.reason.value}")

    def cancel(self, reason: CancellationReason = CancellationReason.USER_REQUESTED) -> bool:
        """Request cancellation.

        This method is typically called by the SDK, not by organ code.

        Args:
            reason: Why the cancellation occurred

        Returns:
            True if this call caused cancellation, False if already cancelled
        """
        if self._cancelled:
            return False

        self._cancelled = True
        self._cancelled_at = time.time()
        self.reason = reason
        self._cancel_event.set()

        logger.info(f"Cancellation requested: request_id={self.request_id}, reason={reason.value}")

        # Execute callbacks (fire and forget)
        for callback in self._callbacks:
            try:
                result = callback()
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                logger.warning(f"Cancellation callback failed: {e}")

        return True

    def on_cancel(self, callback: Callable[[], Any]) -> 'CancellationToken':
        """Register a callback to run when cancelled.

        Callbacks are executed immediately when cancel() is called.
        If already cancelled, callback is executed immediately.

        Args:
            callback: Function to call on cancellation (can be async)

        Returns:
            Self for chaining

        Example:
            token.on_cancel(lambda: cleanup_temp_files())
            token.on_cancel(self.release_lock)
        """
        self._callbacks.append(callback)

        # If already cancelled, execute immediately
        if self._cancelled:
            try:
                result = callback()
                if asyncio.iscoroutine(result):
                    asyncio.create_task(result)
            except Exception as e:
                logger.warning(f"Cancellation callback failed: {e}")

        return self

    async def wait(self) -> None:
        """Wait until cancellation is requested.

        This is useful for background tasks that should run until cancelled.

        Example:
            async def background_worker(token: CancellationToken):
                while True:
                    try:
                        await asyncio.wait_for(token.wait(), timeout=1.0)
                        break  # Cancelled
                    except asyncio.TimeoutError:
                        await do_periodic_work()
        """
        await self._cancel_event.wait()

    async def with_timeout(
        self,
        coro: Coroutine[Any, Any, T],
        timeout: float
    ) -> T:
        """Execute coroutine with both timeout and cancellation support.

        Args:
            coro: Coroutine to execute
            timeout: Maximum time in seconds

        Returns:
            Result of coroutine

        Raises:
            asyncio.CancelledError: If cancelled
            asyncio.TimeoutError: If timeout exceeded

        Example:
            result = await token.with_timeout(
                fetch_data(),
                timeout=30.0
            )
        """
        async def cancellation_waiter():
            await self.wait()
            raise asyncio.CancelledError(f"Request cancelled: {self.reason.value}")

        cancel_task = asyncio.create_task(cancellation_waiter())
        main_task = asyncio.create_task(coro)

        try:
            done, pending = await asyncio.wait(
                [cancel_task, main_task],
                timeout=timeout,
                return_when=asyncio.FIRST_COMPLETED
            )

            # Cancel pending tasks
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass

            # Check results
            if not done:
                raise asyncio.TimeoutError(f"Operation timed out after {timeout}s")

            # Get result from completed task
            for task in done:
                if task is main_task:
                    return task.result()
                elif task is cancel_task:
                    # Cancel task completed means we were cancelled
                    raise asyncio.CancelledError(f"Request cancelled: {self.reason.value}")

            raise RuntimeError("Unexpected state in with_timeout")

        finally:
            # Cleanup
            cancel_task.cancel()
            try:
                await cancel_task
            except asyncio.CancelledError:
                pass

    async def run_until_cancelled(
        self,
        coro: Coroutine[Any, Any, T]
    ) -> Optional[T]:
        """Run coroutine until it completes or cancellation is requested.

        Unlike with_timeout, this doesn't raise on cancellation.

        Args:
            coro: Coroutine to execute

        Returns:
            Result or None if cancelled

        Example:
            result = await token.run_until_cancelled(long_operation())
            if result is None:
                # Was cancelled
                return HandlerResponse(ok=False, error_code="CANCELLED")
        """
        try:
            return await self.with_timeout(coro, timeout=float('inf'))
        except asyncio.CancelledError:
            return None

    @asynccontextmanager
    async def scope(self):
        """Context manager that checks cancellation on entry and exit.

        Example:
            async with token.scope():
                await risky_operation()
                # If cancelled during operation, cleanup happens automatically
        """
        self.check()
        try:
            yield self
        finally:
            # Don't raise on exit, just log
            if self.is_cancelled:
                logger.debug(f"Exiting cancelled scope: request_id={self.request_id}")

    def child(self, name: str = "") -> 'CancellationToken':
        """Create a child token linked to this parent.

        Child tokens are automatically cancelled when parent is cancelled.
        Useful for sub-operations that should be cancelled together.

        Args:
            name: Optional name for debugging

        Returns:
            New child token

        Example:
            parent_token = request.cancellation_token

            # Child for sub-operation
            child = parent_token.child("fetch_data")
            result = await fetch_with_token(child)
        """
        child_token = CancellationToken(
            request_id=f"{self.request_id}:{name}" if name else self.request_id,
            trace_id=self.trace_id,
            _parent=self
        )

        # If parent is already cancelled, cancel child immediately
        if self._cancelled:
            child_token.cancel(CancellationReason.PARENT_CANCELLED)
        else:
            # Cancel child when parent is cancelled
            self.on_cancel(lambda: child_token.cancel(CancellationReason.PARENT_CANCELLED))

        return child_token

    def __bool__(self) -> bool:
        """Allow using token in boolean context.

        Returns True if NOT cancelled (operation should continue).

        Example:
            while token:
                await do_work()
        """
        return not self.is_cancelled


# Convenience factory
def create_token(request_id: str = "", trace_id: str = "") -> CancellationToken:
    """Create a new cancellation token.

    Args:
        request_id: Request identifier
        trace_id: Trace identifier for distributed tracing

    Returns:
        New CancellationToken instance
    """
    return CancellationToken(request_id=request_id, trace_id=trace_id)


# Null token that is never cancelled (for optional cancellation support)
class NullCancellationToken(CancellationToken):
    """A token that is never cancelled.

    Use this as a default when cancellation is optional.
    """

    @property
    def is_cancelled(self) -> bool:
        return False

    def check(self) -> None:
        pass

    def cancel(self, reason: CancellationReason = CancellationReason.USER_REQUESTED) -> bool:
        return False


# Singleton null token
NULL_TOKEN = NullCancellationToken()
