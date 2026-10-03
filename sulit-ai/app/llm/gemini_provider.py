from google import genai
from google.genai import errors, types

from app.llm.base import LLMProvider, LLMProviderError
from app.schemas import ChatMessage


class GeminiProvider(LLMProvider):
    def __init__(
        self,
        model: str,
        api_key: str,
        temperature: float | None,
        max_output_tokens: int,
        timeout: float,
    ) -> None:
        super().__init__(model)
        self._temperature = temperature
        self._max_output_tokens = max_output_tokens
        # google-genai expects the timeout in milliseconds.
        self._client = genai.Client(
            api_key=api_key, http_options=types.HttpOptions(timeout=int(timeout * 1000))
        )

    async def generate(self, messages: list[ChatMessage], system_prompt: str) -> str:
        contents = [
            types.Content(
                role="model" if m.role == "assistant" else "user",
                parts=[types.Part.from_text(text=m.content)],
            )
            for m in messages
        ]
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=self._temperature,
            max_output_tokens=self._max_output_tokens,
        )

        try:
            response = await self._client.aio.models.generate_content(
                model=self.model, contents=contents, config=config
            )
        except errors.APIError as exc:
            raise LLMProviderError(str(exc)) from exc

        if not response.text:
            raise LLMProviderError("Empty response from model.")
        return response.text
