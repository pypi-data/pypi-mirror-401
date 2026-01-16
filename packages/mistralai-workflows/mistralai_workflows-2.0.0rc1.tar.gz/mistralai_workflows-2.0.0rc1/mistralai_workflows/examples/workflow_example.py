import asyncio
from typing import List

import pydantic
import structlog

import mistralai_workflows as workflows
from mistralai_workflows.worker.config import config
from mistralai_workflows.worker.monitoring import setup_logging

logger = structlog.getLogger(__name__)


# Use the real AppConfig from workflows.worker.config


class Result(pydantic.BaseModel):
    results: List[str] = pydantic.Field(description="List of results")


@workflows.activity()
async def my_activity(query: str) -> Result:
    with workflows.task("activity.processing", {"query": query}):
        await asyncio.sleep(1)

    return Result(results=["result1", "result2"])


@workflows.activity()
async def my_long_activity(query: str) -> Result:
    with workflows.task("activity.long_processing", {"query": query}):
        await asyncio.sleep(5)

    return Result(results=["result1", "result2"])


@workflows.activity()
async def my_failing_activity(query: str) -> Result:
    with workflows.task("activity.failing", {"query": query}):
        await asyncio.sleep(1)
        raise Exception("This is a simulated failure")


@workflows.workflow.define(
    name="example-hello-world-workflow",
    workflow_display_name="Hello World",
    workflow_description="Example workflow",
)
class Workflow:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> Result:
        execution_id = workflows.get_execution_id()

        with workflows.task(
            "workflow.execution",
            {"document_title": document_title, "execution_id": execution_id},
        ):
            results = await my_activity(document_title)

        return results


@workflows.workflow.define(name="example-long-hello-world-workflow", workflow_description="Example workflow")
class WorkflowLongExample:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> Result:
        execution_id = workflows.get_execution_id()

        with workflows.task(
            "workflow.long_execution",
            {"document_title": document_title, "execution_id": execution_id},
        ):
            results = await my_long_activity(document_title)

        return results


@workflows.workflow.define(name="example-failing-workflow", workflow_description="Example workflow")
class WorkflowFailingExample:
    @workflows.workflow.entrypoint
    async def run(self, document_title: str) -> Result:
        execution_id = workflows.get_execution_id()
        with workflows.task(
            "workflow.failing_execution",
            {"document_title": document_title, "execution_id": execution_id},
        ):
            results = await my_failing_activity(document_title)

        return results


if __name__ == "__main__":
    setup_logging(
        log_format=config.common.log_format,
        log_level=config.common.log_level,
        app_version=config.common.app_version,
    )
    asyncio.run(workflows.run_worker([Workflow]))
