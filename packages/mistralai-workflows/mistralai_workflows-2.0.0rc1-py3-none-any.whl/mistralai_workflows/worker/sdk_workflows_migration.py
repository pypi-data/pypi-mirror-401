"""
Temporary file for old DX → new DX transition. Remove after migration is complete.
"""

import uuid
from typing import Any, Literal

import mistralai
from pydantic import BaseModel, ConfigDict, Field

from mistralai_workflows.worker.task import task
from mistralai_workflows.worker.workflow import workflow


class _WaitingForInputTaskState(BaseModel):
    """
    Task state broadcasted via streaming when workflow waits for input.

    It's used internally by wait_for_input().

    Clients see this in streaming events and can render a form based on input_schema.
    """

    model_config = ConfigDict(title="waiting_for_input")
    input_schema: dict
    input: Any | None = None


class _SubmitInputParams(BaseModel):
    """
    Request parameters for submitting input.

    Underscore means: Used internally by the update handler.
    """

    custom_task_id: str
    input: Any


class _SubmitInputResult(BaseModel):
    """Response returned to client after submitting input"""

    error: str | None = None


class _PendingInputRequest(BaseModel):
    """
    In-memory tracking of pending input request.

    The has_received_input flag is checked by wait_condition().
    """

    custom_task_id: str
    input_schema: type[BaseModel]
    has_received_input: bool = False
    input: Any | None = None


class workflows:
    class InteractiveWorkflow:
        """
        Base class for workflows that need to wait for external input.

        Example usage:
            @workflow.define(name="my-workflow")
            class MyWorkflow(workflows.BaseWorkflow):
                @workflow.entrypoint
                async def run(self, params: MyInput):
                    # Ask human for approval
                    approval = await self.wait_for_input(ApprovalSchema)
                    if approval.approved:
                        return "Approved!"
                    return "Denied"

        How to submit input (from external client):
            client.update_workflow(
                execution_id="wf-123",
                update_name="submit_input",
                params={"custom_task_id": "task-456", "input": {"approved": True}}
            )
        """

        def __init__(self) -> None:
            # In-memory storage: tracks which tasks are waiting for input
            self.__pending_inputs: dict[str, _PendingInputRequest] = {}

        async def wait_for_input[T: BaseModel](self, schema: type[T]) -> T:
            """
            PAUSE workflow and wait for external input matching the schema.

            This creates a visible task in the streaming API that clients can see.
            The workflow execution is suspended until input is submitted via the
            submit_input update handler.

            Args:
                schema: Pydantic model defining expected input structure

            Returns:
                Validated input matching the schema

            How the WAKE UP works:
            1. We store a flag (has_received_input = False) in memory
            2. wait_condition() pauses workflow, checking flag on every event
            3. External source calls submit_input update → sets flag = True
            4. That API call is an EVENT → Temporal re-checks the condition
            5. Condition now True → workflow resumes!
            """
            with task("wait_for_input", state=_WaitingForInputTaskState(input_schema=schema.model_json_schema())) as t:
                pending_request = _PendingInputRequest(
                    custom_task_id=t.id,
                    input_schema=schema,
                )
                self.__pending_inputs[t.id] = pending_request

                await workflow.wait_condition(lambda: self.__pending_inputs[t.id].has_received_input)

                input_value = pending_request.input
                validated_input = schema.model_validate(input_value)

                t.update_state(updates={"input": validated_input})

            return validated_input

        @workflow.update(name="__internal_submit_input__")
        async def _handle_input_submission(
            self,
            params: _SubmitInputParams,
        ) -> _SubmitInputResult:
            """
            Called by external API when external input is submitted.

            Flow:
            1. External client calls: client.update_workflow(execution_id, "submit_input", {...})
            2. Temporal routes update to this handler
            3. This handler sets: has_received_input = True
            4. Setting that flag is an EVENT → Temporal re-evaluates wait_condition()
            5. wait_condition() sees flag is True → workflow resumes!

            Args:
                params: Contains task_id and input data from external source

            Returns:
                Result with error message if validation fails
            """
            pending_request = self.__pending_inputs.get(params.custom_task_id)
            if not pending_request:
                return _SubmitInputResult(error=f"No pending input request found for task {params.custom_task_id}")

            try:
                pending_request.input_schema.model_validate(params.input)
            except Exception as e:
                return _SubmitInputResult(error=f"Invalid input for task {params.custom_task_id}: {str(e)}")

            pending_request.input = params.input
            pending_request.has_received_input = True

            return _SubmitInputResult()

    class contributions:
        # simulate proper mistralai contribution
        class workflows_mistralai:
            UserMessage = mistralai.UserMessage
            AssistantMessage = mistralai.AssistantMessage
            Messages = mistralai.Messages

            Mistral = mistralai.Mistral
            ChatCompletionRequest = mistralai.ChatCompletionRequest

            class LeChatPayloadWorking(BaseModel):
                model_config = ConfigDict(title="working")

                type: Literal["tool", "thinking"] | str = "tool"
                title: str
                content: str

            class LeChatPayloadAssistantMessage(BaseModel):
                model_config = ConfigDict(title="assistant_message")

                role: Literal["assistant"] = "assistant"
                content: str = Field(default="", description="Assistant message content")

            class LeChatPayloadUserMessage(BaseModel):
                model_config = ConfigDict(title="user_message")

                role: Literal["user"] = "user"
                content: str = Field(default="", description="User message to continue the conversation")

            class LeChatMarkdownOutput(BaseModel):
                mime_type: Literal["text/markdown"] = "text/markdown"
                content: str
                uri: str = Field(default_factory=lambda: f"file://markdown/{uuid.uuid4()}.md")

            class LeChatOutput(BaseModel):
                outputs: """list[
                    workflows_mistralai.LeChatPayloadAssistantMessage
                    | workflows_mistralai.LeChatPayloadUserMessage
                    | workflows_mistralai.LeChatMarkdownOutput
                ]""" = Field(default_factory=list)


# simulate `from workflows.contributions import workflows_mistralai`
workflows_mistralai = workflows.contributions.workflows_mistralai
