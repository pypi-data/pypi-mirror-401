import asyncio

import mistralai_workflows as workflows
from mistralai_workflows.examples.workflow_example import Workflow as WorkflowExample
from mistralai_workflows.examples.workflow_insurance_claims import InsuranceClaimsWorkflow
from mistralai_workflows.examples.workflow_multi_turn_chat import MultiTurnChatWorkflow

if __name__ == "__main__":
    asyncio.run(workflows.run_worker([WorkflowExample, InsuranceClaimsWorkflow, MultiTurnChatWorkflow]))
