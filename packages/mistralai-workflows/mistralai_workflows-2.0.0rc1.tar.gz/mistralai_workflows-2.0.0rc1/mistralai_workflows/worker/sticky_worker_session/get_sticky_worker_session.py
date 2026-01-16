import structlog
import temporalio
import temporalio.workflow

from mistralai_workflows.worker.activity import activity

from .sticky_worker_session import StickyWorkerSession

logger = structlog.get_logger(__name__)

GET_STICKY_WORKER_SESSION_ACTIVITY_NAME = "get_sticky_worker_session"


@activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
async def get_sticky_worker_session() -> StickyWorkerSession:
    """
    Get sticky worker session to execute activities in the same worker.

    Example:
    ```
    async with run_sticky_worker_session(await get_sticky_worker_session()):
        await some_activity() # Will be executed in the same worker
        await some_activity() # Will be executed in the same worker
        await some_activity() # Will be executed in the same worker
    ```

    Returns:
        StickyWorkerSession: The sticky worker session.

    Raises:
        NotImplementedError: Always, as this should never be called directly.
    """
    if temporalio.workflow.in_workflow():
        raise NotImplementedError("This activity should never be called directly")

    return StickyWorkerSession(task_queue="local")
