from anthropic import AnthropicError, AsyncAnthropic

from app.llm.base import LLMProvider, LLMProviderError
from app.schemas import ChatMessage


class AnthropicProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str | None,
        temperature: float | None,
        max_output_tokens: int,
        timeout: float,
    ) -> None:
        super().__init__(model)
        self._temperature = temperature
        self._max_output_tokens = max_output_tokens
        self._client = AsyncAnthropic(api_key=api_key, base_url=base_url, timeout=timeout)

    async def generate(self, messages: list[ChatMessage], system_prompt: str) -> str:
        kwargs = {}
        if self._temperature is not None:
            kwargs["temperature"] = min(self._temperature, 1.0)

        try:
            response = await self._client.messages.create(
                model=self.model,
                system=system_prompt,
                max_tokens=self._max_output_tokens,
                messages=[{"role": m.role, "content": m.content} for m in messages],
                **kwargs,
            )
        except AnthropicError as exc:
            raise LLMProviderError(str(exc)) from exc

        text = "".join(block.text for block in response.content if block.type == "text")
        if not text:
            raise LLMProviderError("Empty response from model.")
        return text

    async def aclose(self) -> None:
        await self._client.close()
