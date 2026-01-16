from typing import Any, cast

from pydantic import BaseModel

from mistralai_workflows.worker.task.protocol import StatefulTaskProtocol
from mistralai_workflows.worker.task.task import Task


def _infer_task_type_from_state(state: Any) -> str | None:
    """Attempt to infer task type from state object."""
    if isinstance(state, BaseModel):
        # Use model_config.title if available
        title = state.model_config.get("title")
        if title:
            return title
        return type(state).__name__

    if hasattr(state, "__dataclass_fields__"):
        # Dataclass: use class name
        return type(state).__name__

    if isinstance(state, dict):
        # Cannot infer type from dict
        return None

    # For other typed objects, use class name
    if hasattr(state, "__class__") and not isinstance(state, (str, int, float, bool, list, tuple, set)):
        return type(state).__name__

    return None


def task_from[T](state: T, type: str | None = None) -> StatefulTaskProtocol[T]:
    """
    Create a stateful task, inferring type from state when not provided.

    Args:
        state: Initial state (required). Type is inferred from Pydantic models or dataclasses.
        type: Explicit task type. If None, inferred from state.

    Returns:
        StatefulTaskProtocol: Task with state management methods (`set_state()`, `update_state()`).

    Raises:
        ValueError: If type cannot be inferred (e.g., dict or primitive state without explicit type).

    Examples:
        >>> class ProcessingState(BaseModel):
        ...     model_config = ConfigDict(title="document_processing")
        ...     progress: float = 0.0

        >>> with task_from(ProcessingState()) as t:  # type="document_processing"
        ...     t.update_state({"progress": 0.5})

        >>> with task_from({"progress": 0}, type="export") as t:  # Explicit type required for dict
        ...     t.update_state({"progress": 100})
    """
    if type is None:
        inferred = _infer_task_type_from_state(state)
        if not inferred:
            raise ValueError(
                "Could not infer task type from state (e.g. dict or primitive). Please pass an explicit type argument."
            )
        type = inferred

    return cast(StatefulTaskProtocol[T], Task[T](type=type, state=state))
