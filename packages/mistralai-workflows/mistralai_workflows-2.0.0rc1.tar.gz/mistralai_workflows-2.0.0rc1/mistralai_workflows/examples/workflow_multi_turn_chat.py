import asyncio
import os
from itertools import count

import mistralai

# Import actual types for type checking
from mistralai import AssistantMessage, ChatCompletionRequest, Messages, Mistral

import mistralai_workflows as workflows
from mistralai_workflows import workflows_mistralai


class WorkflowParams(workflows_mistralai.LeChatPayloadUserMessage):
    model: str = "mistral-medium-2508"


# Type aliases for better type checking
# UserMessage = UserMessage
# AssistantMessage = AssistantMessage
# Messages = Messages
# Mistral = Mistral
# ChatCompletionRequest = ChatCompletionRequest


@workflows.workflow.define(
    name="multi_turn_chat_workflow",
    workflow_description="Multi-turn chat workflow using Mistral AI",
)
class MultiTurnChatWorkflow(workflows.workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> None:
        initial_message = workflows_mistralai.LeChatPayloadUserMessage(content=params.content)

        messages: list[Messages] = []
        with workflows.task_from(
            state=workflows_mistralai.LeChatPayloadWorking(title="Conversation", content="")
        ) as task:
            for i in count():
                task.update_state(updates={"title": f"Waiting for user input ({i + 1} steps)", "content": ""})
                user_message = (
                    await self.wait_for_input(workflows_mistralai.LeChatPayloadUserMessage)
                    if i > 0
                    else initial_message
                )

                task.update_state(updates={"title": f"Generating assistant response ({i + 1} steps)", "content": ""})
                messages.append(mistralai.UserMessage.model_validate(user_message.model_dump()))
                assistant_message = await generate_response(
                    ChatCompletionRequest(model=params.model, messages=messages)
                )
                messages.append(assistant_message)


def get_mistral_client() -> Mistral:
    return Mistral(api_key=os.getenv("PROD_MISTRAL_API_KEY") or os.getenv("MISTRAL_API_KEY"))


@workflows.activity()
async def generate_response(
    params: ChatCompletionRequest,
    mistral_client: Mistral = workflows.Depends(get_mistral_client),
) -> AssistantMessage:
    with workflows.task_from(state=workflows_mistralai.LeChatPayloadAssistantMessage()) as task:
        mistral_stream = await mistral_client.chat.stream_async(
            **params.model_copy(update={"stream": True}).model_dump(by_alias=True)
        )
        async for chunk in mistral_stream.generator:
            if chunk.data.choices[0].delta.content:
                assert isinstance(chunk.data.choices[0].delta.content, str), "Non string content is not supported"
                new_content = task.state.content + chunk.data.choices[0].delta.content
                task.update_state(updates={"content": new_content})
        return AssistantMessage.model_validate(task.state, from_attributes=True)


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([MultiTurnChatWorkflow]))
