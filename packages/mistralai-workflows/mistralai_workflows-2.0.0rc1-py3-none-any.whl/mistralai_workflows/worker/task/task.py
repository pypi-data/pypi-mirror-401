import uuid
from typing import Any, Type

import structlog
import temporalio.workflow
from pydantic import BaseModel, TypeAdapter
from pydantic_core import PydanticSerializationError

from mistralai_workflows.protocol.v1.events import (
    CustomTaskCompleted,
    CustomTaskCompletedAttributes,
    CustomTaskFailed,
    CustomTaskFailedAttributes,
    CustomTaskInProgress,
    CustomTaskInProgressAttributes,
    CustomTaskStarted,
    CustomTaskStartedAttributes,
    Failure,
    JSONPatchPayload,
    JSONPayload,
    WorkflowEvent,
)
from mistralai_workflows.worker.events.event_context import EventContext
from mistralai_workflows.worker.events.event_utils import create_base_event_fields, should_publish_event
from mistralai_workflows.worker.events.json_patch import make_json_patch

logger = structlog.get_logger(__name__)

adapter: TypeAdapter[Any] = TypeAdapter(Any)


def _to_json(obj: Any) -> Any:
    return adapter.dump_python(obj, mode="json")


def _publish_task_event(event: WorkflowEvent) -> None:
    context = EventContext.get_singleton()
    if context is None:
        if not should_publish_event():
            return
        raise RuntimeError(
            "EventContext not initialized - ensure the Workflows client is enabled and EventContext is active"
        )

    context.publish_event(event)


class Task[T]:
    """
    Observable task context manager that emits lifecycle events to the Workflows API.

    Lifecycle: Started → InProgress* → Completed|Failed

    Use for operations that need real-time observability (LLM streaming, file processing, etc).
    """

    _id: str
    _type: str
    _state: T | None
    _started: bool

    def __init__(self, type: str, state: T | None = None) -> None:
        self._id = str(temporalio.workflow.uuid4() if temporalio.workflow.in_workflow() else uuid.uuid4())
        self._type = type
        self._state = state
        self._started = False

    @property
    def id(self) -> str:
        return self._id

    @property
    def type(self) -> str:
        return self._type

    @property
    def state(self) -> T | None:
        return self._state

    def __enter__(self) -> "Task[T]":
        if not should_publish_event():
            return self

        # Emit CUSTOM_TASK_STARTED event
        _publish_task_event(
            CustomTaskStarted(
                **create_base_event_fields(),
                attributes=CustomTaskStartedAttributes(
                    custom_task_id=self._id,
                    custom_task_type=self._type,
                    payload=JSONPayload(value=_to_json(self._state)),
                ),
            )
        )

        return self

    def __exit__(self, exc_type: Type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        if not should_publish_event():
            return

        if exc_type is None:
            _publish_task_event(
                CustomTaskCompleted(
                    **create_base_event_fields(),
                    attributes=CustomTaskCompletedAttributes(
                        custom_task_id=self._id,
                        custom_task_type=self._type,
                        payload=JSONPayload(value=_to_json(self._state)),
                    ),
                )
            )
        else:
            _publish_task_event(
                CustomTaskFailed(
                    **create_base_event_fields(),
                    attributes=CustomTaskFailedAttributes(
                        custom_task_id=self._id,
                        custom_task_type=self._type,
                        failure=Failure(message=str(exc_val)),
                    ),
                )
            )

    def set_state(self, state: T) -> None:
        """Update state, emitting InProgress with JSON patch or full payload."""
        if self._state is None:
            raise RuntimeError("Cannot set_state() on task created without state")

        previous = self._state
        self._state = state

        if not should_publish_event():
            return

        try:
            patches = make_json_patch(previous, state)
            _publish_task_event(
                CustomTaskInProgress(
                    **create_base_event_fields(),
                    attributes=CustomTaskInProgressAttributes(
                        custom_task_id=self._id,
                        custom_task_type=self._type,
                        payload=JSONPatchPayload(value=patches),
                    ),
                )
            )
        except PydanticSerializationError:
            logger.error(
                "Failed JSON patch - state updated locally but not published",
                previous=previous,
                new=state,
                task_id=self._id,
            )

    def update_state(self, updates: dict[str, Any]) -> None:
        """Partial state update (only for BaseModel or dict)."""
        if self._state is None:
            raise RuntimeError("Cannot update_state() on task created without state")

        if isinstance(self._state, BaseModel):
            self.set_state(self._state.model_copy(update=updates))
        elif isinstance(self._state, dict):
            new_dict: dict[str, Any] = self._state.copy()
            new_dict.update(updates)
            self.set_state(new_dict)  # type: ignore
        else:
            raise TypeError(f"update_state() requires BaseModel or dict, got {type(self._state).__name__}")
