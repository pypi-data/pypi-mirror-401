import asyncio
import os
from textwrap import dedent
from typing import List, Literal

import mistralai

# Import actual mistralai types for proper type checking
from mistralai import AssistantMessage, SystemMessage, ToolMessage, UserMessage
from pydantic import BaseModel, Field

import mistralai_workflows as workflows
from mistralai_workflows import workflows_mistralai


class ClaimType(BaseModel):
    claim_type: Literal["medical", "auto_accident", "other"] = "other"


class ClaimStatus(BaseModel):
    status: Literal["approved", "rejected", "pending"] = "pending"


class ClaimResponseSignalParams(BaseModel):
    is_approved: bool = Field(description="Whether the claim is approved or rejected", default=False)


class WorkflowParams(BaseModel):
    attachement_urls: List[str] = Field(
        default_factory=lambda: [
            "https://raw.githubusercontent.com/mistralai/cookbook/refs/heads/main/mistral/ocr/receipt.png"
        ]
    )
    email_content: str = Field(
        default=(
            "Hello, I'm John Doe. I'm calling about my medical claim for my surgery on December 10, 2025. "
            "I had a surgery on my knee and I'm not sure if I'll be able to work after that."
        )
    )


class WorkflowOutput(BaseModel):
    final_email: str


@workflows.workflow.define(
    name="insurance_claims_workflow",
    workflow_description="Workflow to process insurance claims",
)
class InsuranceClaimsWorkflow(workflows.workflows.InteractiveWorkflow):
    @workflows.workflow.entrypoint
    async def run(self, params: WorkflowParams) -> workflows_mistralai.LeChatOutput:
        # Extract attachments content (OCR)
        attachements_content: dict[str, str] = {}
        if params.attachement_urls:
            with workflows.task_from(
                state=workflows_mistralai.LeChatPayloadWorking(title="OCR attachments", content="")
            ) as task:
                ocr_tasks = [llm_ocr_from_url(MistralOCRParams(url=url)) for url in params.attachement_urls]
                responses = await asyncio.gather(*ocr_tasks)
                task.update_state(
                    updates={"title": "OCR attachments", "content": f"Processed {len(responses)} documents"}
                )
            attachements_content = {
                url: "\n\n".join([page.markdown for page in response.pages])
                for url, response in zip(params.attachement_urls, responses, strict=True)
            }

        # Build full email with attachments
        documents = "\n\n".join(f"--- Document: {url}\n\n{markdown}" for url, markdown in attachements_content.items())
        full_email = dedent(
            f"""
            <received_email>
            {params.email_content}
            </received_email>

            <received_attachments>
            {documents}
            </received_attachments>
            """
        )

        # Classify claim type
        with workflows.task_from(
            state=workflows_mistralai.LeChatPayloadWorking(title="Categorizing claim", content="")
        ) as task:
            try:
                claim_type = await llm_classify_claim_type(LLMClassifyClaimTypeParams(full_email=full_email))
            except Exception:
                claim_type = await self.wait_for_input(ClaimType)
            task.update_state(updates={"title": "Categorizing claim", "content": claim_type.claim_type})

        # Predict claim status
        with workflows.task_from(
            state=workflows_mistralai.LeChatPayloadWorking(title="Predicting claim status", content="")
        ) as task:
            if claim_type.claim_type == "auto_accident":
                # Auto-approve auto accident claims
                claim_status = ClaimStatus(status="approved")
            elif claim_type.claim_type == "medical":
                # Ask for human feedback for medical claims
                claim_status = await self.wait_for_input(ClaimStatus)
            elif claim_type.claim_type == "other":
                # Reject other claims
                claim_status = ClaimStatus(status="rejected")
            else:
                raise ValueError("Invalid claim category")
            task.update_state(updates={"results": claim_status.status})

        # Generate final email
        final_email = await llm_generate_final_email(
            GenerateEmailParams(full_email=full_email, claim_status=claim_status)
        )
        return workflows_mistralai.LeChatOutput(
            outputs=[workflows_mistralai.LeChatMarkdownOutput(content=final_email.content)]
        )


def get_mistral_client() -> mistralai.Mistral:
    return mistralai.Mistral(api_key=os.getenv("PROD_MISTRAL_API_KEY") or os.getenv("MISTRAL_API_KEY"))


class LLMClassifyClaimTypeParams(BaseModel):
    full_email: str


@workflows.activity()
async def llm_classify_claim_type(
    params: LLMClassifyClaimTypeParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> ClaimType:
    with workflows.task_from(
        state=workflows_mistralai.LeChatPayloadAssistantMessage(content="Classifying claim type...")
    ) as task:
        result = await mistral_client.chat.parse_async(
            model="mistral-medium-latest",
            messages=[
                SystemMessage(content="Given the following claim, extract the category of the claim."),
                UserMessage(content=params.full_email),
            ],
            response_format=ClaimType,
        )
        if not result.choices or not result.choices[0].message or not result.choices[0].message.parsed:
            task.update_state(updates={"content": "Failed to classify claim type"})
            raise ValueError("No response from Mistral")
        else:
            parsed = result.choices[0].message.parsed
            task.update_state(updates={"content": parsed.model_dump_json(indent=2)})
            return parsed


class GenerateEmailParams(BaseModel):
    full_email: str
    claim_status: ClaimStatus


class GenerateEmailResult(BaseModel):
    content: str


@workflows.activity()
async def llm_generate_final_email(
    params: GenerateEmailParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> GenerateEmailResult:
    with workflows.task_from(state=workflows_mistralai.LeChatPayloadAssistantMessage()) as task:
        # with workflows.task_from() as task:
        messages: list[AssistantMessage | SystemMessage | ToolMessage | UserMessage] = [
            SystemMessage(content="Generate a short email to the customer with the claim conclusion."),
            UserMessage(
                content=dedent(
                    f"""
                    The claim has been {params.claim_status.status}.
                    Sign the email with 'Best regards, Insurance Company'.
                    Here is the original claim information:

                    {params.full_email}
                    """
                )
            ),
        ]
        stream = await mistral_client.chat.stream_async(
            model="mistral-medium-2508",
            messages=messages,
        )
        async for chunk in stream.generator:
            if chunk.data.choices[0].delta.content:
                assert isinstance(chunk.data.choices[0].delta.content, str), "Non string content is not supported"
                new_content = task.state.content + chunk.data.choices[0].delta.content
                task.update_state(updates={"content": new_content})

        return GenerateEmailResult(content=task.state.content)


class MistralOCRParams(BaseModel):
    mistral_model: str = "mistral-ocr-latest"
    url: str


@workflows.activity()
async def llm_ocr_from_url(
    params: MistralOCRParams,
    mistral_client: mistralai.Mistral = workflows.Depends(get_mistral_client),
) -> mistralai.OCRResponse:
    """Perform OCR on a document using Mistral's OCR API."""
    document = mistralai.DocumentURLChunk(document_url=params.url)
    response = await mistral_client.ocr.process_async(
        model=params.mistral_model,
        document=document,
        include_image_base64=True,
    )
    return response


if __name__ == "__main__":
    asyncio.run(workflows.run_worker([InsuranceClaimsWorkflow]))
