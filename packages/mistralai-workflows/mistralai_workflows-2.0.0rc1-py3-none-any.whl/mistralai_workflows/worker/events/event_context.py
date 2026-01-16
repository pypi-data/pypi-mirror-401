import asyncio
from contextvars import ContextVar, Token
from typing import Any, Coroutine, Optional

import structlog

from mistralai_workflows.client import WorkflowsClient
from mistralai_workflows.protocol.v1.events import WorkflowEvent
from mistralai_workflows.worker.utils import reset_contextvar

logger = structlog.get_logger(__name__)

# PROBLEM: We want to publish events to the Workflows API from within Temporal workflows, but Temporal
# sandboxes workflows from asyncio (no event loop access, no IO) to enforce deterministic replay.
#
# SOLUTION: Store an EventContext (WorkflowsClient + TaskGroup) as a global singleton, created by the
# main worker before running workflows. Workflows call `EventContext.get_singleton().publish_event()`
# which schedules IO on the worker's asyncio loop—outside Temporal's sandbox.
#
# WHY GLOBAL (not contextvars)? Temporal clears contextvars between workflow/activity boundaries.
# The contextvar `_is_event_context_singleton_owner` only tracks who created the singleton for cleanup.
_event_context_singleton: Optional["EventContext"] = None
_is_event_context_singleton_owner: ContextVar[bool] = ContextVar("is_event_context_singleton_owner", default=False)


class EventContext:
    """Context for publishing workflow events to the Workflows API in the background.

    This context manages a TaskGroup for non-blocking event publishing, similar to StreamingContext.
    Events are published asynchronously to avoid adding latency to workflow execution.
    """

    def __init__(self, workflows_client: WorkflowsClient):
        self.workflows_client = workflows_client
        self._tg = asyncio.TaskGroup()
        self._token: Optional[Token] = None
        self._send_lock = asyncio.Lock()

    @staticmethod
    def get_singleton() -> Optional["EventContext"]:
        """Get the current event context singleton."""
        return _event_context_singleton

    async def __aenter__(self) -> "EventContext":
        """Enter the event context, setting it as the singleton."""
        global _event_context_singleton
        if _event_context_singleton is not None:
            return _event_context_singleton

        self._token = _is_event_context_singleton_owner.set(True)
        _event_context_singleton = self
        await self._tg.__aenter__()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the event context, cleaning up resources."""
        global _event_context_singleton
        if not _is_event_context_singleton_owner.get():
            return

        try:
            await self._tg.__aexit__(exc_type, exc_val, exc_tb)
        finally:
            assert self._token, "Should have token because _is_event_context_singleton_owner is True"
            reset_contextvar(_is_event_context_singleton_owner, self._token)
            _event_context_singleton = None

    def _safe_add_task_to_task_group(self, coro: Coroutine) -> None:
        """Safely add a coroutine to the task group with error handling.

        This wraps the coroutine in a try-except block to prevent task group
        from being cancelled if the task raises an exception.
        """

        async def wrapped() -> None:
            try:
                await coro
            except Exception as e:
                logger.error(
                    "Task failed in event context",
                    error=str(e),
                    task=coro.__name__ if hasattr(coro, "__name__") else str(coro),
                )

        self._tg.create_task(wrapped())

    async def _send_event(self, event: WorkflowEvent) -> None:
        """Send event to the API with lock to ensure sequential sending."""
        async with self._send_lock:
            try:
                await self.workflows_client.send_event(event)
            except Exception as e:
                logger.warning(
                    "Failed to send workflow event",
                    event_type=event.event_type,
                    error=str(e),
                )

    def publish_event(self, event: WorkflowEvent) -> None:
        """Publish a workflow event in the background.

        This method does not block - it schedules the event to be published
        asynchronously via the task group.
        """
        if self._token is None:
            raise RuntimeError("EventContext not entered")

        self._safe_add_task_to_task_group(self._send_event(event))
