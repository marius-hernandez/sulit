from openai import AsyncOpenAI, OpenAIError

from app.llm.base import LLMProvider, LLMProviderError
from app.schemas import ChatMessage


class OpenAIProvider(LLMProvider):
    """Works with OpenAI and any OpenAI-compatible API (e.g. Ollama's /v1 endpoint)."""

    def __init__(
        self,
        model: str,
        api_key: str,
        base_url: str | None,
        temperature: float | None,
        timeout: float,
    ) -> None:
        super().__init__(model)
        self._temperature = temperature
        self._client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout)

    async def generate(self, messages: list[ChatMessage], system_prompt: str) -> str:
        payload = [{"role": "system", "content": system_prompt}]
        payload += [{"role": m.role, "content": m.content} for m in messages]

        kwargs = {}
        if self._temperature is not None:
            kwargs["temperature"] = self._temperature

        try:
            response = await self._client.chat.completions.create(
                model=self.model, messages=payload, **kwargs
            )
        except OpenAIError as exc:
            raise LLMProviderError(str(exc)) from exc

        content = response.choices[0].message.content if response.choices else None
        if not content:
            raise LLMProviderError("Empty response from model.")
        return content

    async def aclose(self) -> None:
        await self._client.close()
