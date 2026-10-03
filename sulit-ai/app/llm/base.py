from abc import ABC, abstractmethod

from app.schemas import ChatMessage


class LLMProviderError(Exception):
    """Raised when the upstream LLM call fails."""


class LLMProvider(ABC):
    def __init__(self, model: str) -> None:
        self.model = model

    @abstractmethod
    async def generate(self, messages: list[ChatMessage], system_prompt: str) -> str:
        """Return the assistant reply for the given conversation."""

    async def aclose(self) -> None:  # noqa: B027 - optional hook
        """Release underlying HTTP resources."""
