from typing import Any, Generator
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from mistralai_workflows import InteractiveWorkflow, workflow


@pytest.fixture
def mock_should_publish_event() -> Generator[Any, None, None]:
    """Mock should_publish_event for interactive workflow tests.

    This prevents EventContext initialization errors since tests don't run
    with a real WorkflowsClient. Only use this fixture for interactive workflow tests.
    """
    with patch("mistralai_workflows.worker.task.task.should_publish_event", return_value=False) as mock:
        yield mock


class ApprovalInput(BaseModel):
    approved: bool
    reason: str


class ApprovalResult(BaseModel):
    status: str
    reason: str


class MultiStepResult(BaseModel):
    approvals: list[str]
    final_status: str


@workflow.define(name="simple_approval_workflow")
class SimpleApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str, description: str = "Test request") -> ApprovalResult:
        approval = await self.wait_for_input(ApprovalInput, label="Approval Request")

        if approval.approved:
            return ApprovalResult(status="approved", reason=approval.reason)
        else:
            return ApprovalResult(status="rejected", reason=approval.reason)


@workflow.define(name="multi_step_approval_workflow")
class MultiStepApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str) -> MultiStepResult:
        approvals = []

        approval1 = await self.wait_for_input(ApprovalInput, label="Manager Approval")
        approvals.append(f"Step 1: {'approved' if approval1.approved else 'rejected'} - {approval1.reason}")

        approval2 = await self.wait_for_input(ApprovalInput, label="Executive Approval")
        approvals.append(f"Step 2: {'approved' if approval2.approved else 'rejected'} - {approval2.reason}")

        all_approved = approval1.approved and approval2.approved
        return MultiStepResult(approvals=approvals, final_status="approved" if all_approved else "rejected")


@workflow.define(name="stateful_approval_workflow")
class StatefulApprovalWorkflow(InteractiveWorkflow):
    def __init__(self) -> None:
        super().__init__()
        self.approvals_received: list[str] = []
        self.status: str = "pending"

    @workflow.entrypoint
    async def run(self, request_id: str) -> ApprovalResult:
        self.status = "waiting_for_approval"

        approval = await self.wait_for_input(ApprovalInput, label="State Tracked Approval")
        self.approvals_received.append(approval.reason)
        self.status = "approved" if approval.approved else "rejected"

        return ApprovalResult(status=self.status, reason=f"Processed {len(self.approvals_received)} approvals")


@workflow.define(name="parallel_approval_workflow")
class ParallelApprovalWorkflow(InteractiveWorkflow):
    @workflow.entrypoint
    async def run(self, request_id: str) -> MultiStepResult:
        import asyncio

        approval1_task = asyncio.create_task(self.wait_for_input(ApprovalInput, label="Manager Approval"))
        approval2_task = asyncio.create_task(self.wait_for_input(ApprovalInput, label="Executive Approval"))

        approval1, approval2 = await asyncio.gather(approval1_task, approval2_task)

        approvals = [
            f"Manager: {'approved' if approval1.approved else 'rejected'} - {approval1.reason}",
            f"Executive: {'approved' if approval2.approved else 'rejected'} - {approval2.reason}",
        ]

        all_approved = approval1.approved and approval2.approved
        return MultiStepResult(approvals=approvals, final_status="approved" if all_approved else "rejected")
