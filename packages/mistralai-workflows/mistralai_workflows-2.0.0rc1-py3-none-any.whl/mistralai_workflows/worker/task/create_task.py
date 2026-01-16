from typing import overload

from mistralai_workflows.worker.task.protocol import StatefulTaskProtocol, StatelessTaskProtocol
from mistralai_workflows.worker.task.task import Task


@overload
def task(type: str) -> StatelessTaskProtocol: ...


@overload
def task[T](type: str, state: T) -> StatefulTaskProtocol[T]: ...


def task[T](type: str, state: T | None = None) -> StatelessTaskProtocol | StatefulTaskProtocol[T]:
    """
    Create an observable task that emits lifecycle events.

    Tasks track bounded operations (LLM streaming, file processing, agent traces) with
    clear start/end boundaries for UI and observability.

    Args:
        type: Task type identifier.
        state: Initial state. When provided, enables `set_state()` and `update_state()` methods.

    Returns:
        StatefulTaskProtocol: When state is provided - includes state management methods.
        StatelessTaskProtocol: When state is omitted - lifecycle events only.

    Examples:
        Stateless (lifecycle events only):
        >>> with task("cleanup"):
        ...     do_cleanup()

        Stateful with dict:
        >>> with task("export", state={"progress": 0}) as t:
        ...     t.update_state({"progress": 50})  # Partial update
        ...     t.set_state({"progress": 100})    # Full replacement

        Stateful with Pydantic model:
        >>> class ExportState(BaseModel):
        ...     progress: int = 0
        ...     status: str = "pending"

        >>> with task("export", state=ExportState()) as t:
        ...     t.update_state({"progress": 50, "status": "processing"})
        ...     t.set_state(ExportState(progress=100, status="done"))
    """
    return Task[T](type=type, state=state)
