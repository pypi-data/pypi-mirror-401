import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, List, Type

import structlog
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def create_test_worker(
    env: WorkflowEnvironment,
    workflows: List[Type],
    activities: List[Callable] | None = None,
    task_queue: str = "test-task-queue",
) -> AsyncGenerator[Worker, None]:
    worker = Worker(
        env.client,
        task_queue=task_queue,
        workflows=workflows,
        activities=activities or [],
    )

    async with worker:
        yield worker


async def execute_workflow_in_test_env(
    env: WorkflowEnvironment,
    workflow_class: Type,
    workflow_input: Any,
    workflow_id: str | None = None,
    task_queue: str = "test-task-queue",
) -> Any:
    from mistralai_workflows.worker.workflow_definition import get_workflow_definition

    workflow_def: Any = get_workflow_definition(workflow_class)
    if not workflow_def:
        raise ValueError(f"Workflow {workflow_class} is not properly decorated")

    handle = await env.client.start_workflow(
        workflow_def.name,
        workflow_input,
        id=workflow_id or f"test-workflow-{asyncio.current_task().get_name()}",  # type: ignore
        task_queue=task_queue,
    )

    return await handle.result()
