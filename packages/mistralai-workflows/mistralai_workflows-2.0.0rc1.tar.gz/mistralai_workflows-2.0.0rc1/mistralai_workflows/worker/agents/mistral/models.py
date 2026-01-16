import mistralai
from pydantic import BaseModel


class ChatStreamState(BaseModel):
    content: str = ""


class ConversationStreamState(BaseModel):
    content: str = ""


class ConversationAppendRequest(mistralai.ConversationAppendRequest):
    conversation_id: str


class AgentUpdateRequest(mistralai.AgentUpdateRequest):
    agent_id: str
