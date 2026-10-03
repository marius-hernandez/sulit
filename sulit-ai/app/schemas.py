from typing import Literal

from pydantic import BaseModel, Field, field_validator

Role = Literal["user", "assistant"]


class ChatMessage(BaseModel):
    role: Role
    content: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(min_length=1, max_length=100)

    @field_validator("messages")
    @classmethod
    def _last_message_from_user(cls, messages: list[ChatMessage]) -> list[ChatMessage]:
        if messages[-1].role != "user":
            raise ValueError("The last message must be from the user.")
        return messages


class ChatResponse(BaseModel):
    reply: str
    model: str
