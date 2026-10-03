from app.config import Settings
from app.llm.base import LLMProvider

OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434/v1"


def create_provider(settings: Settings) -> LLMProvider:
    api_key = settings.llm_api_key.get_secret_value() if settings.llm_api_key else ""

    # Imports are local so only the selected provider's SDK is loaded.
    match settings.llm_provider:
        case "openai" | "ollama":
            from app.llm.openai_provider import OpenAIProvider

            is_ollama = settings.llm_provider == "ollama"
            return OpenAIProvider(
                model=settings.llm_model,
                # Ollama ignores the key, but the OpenAI SDK requires a non-empty value.
                api_key=api_key or ("ollama" if is_ollama else ""),
                base_url=settings.llm_base_url or (OLLAMA_DEFAULT_BASE_URL if is_ollama else None),
                temperature=settings.llm_temperature,
                timeout=settings.llm_timeout_seconds,
            )
        case "anthropic":
            from app.llm.anthropic_provider import AnthropicProvider

            return AnthropicProvider(
                model=settings.llm_model,
                api_key=api_key,
                base_url=settings.llm_base_url,
                temperature=settings.llm_temperature,
                max_output_tokens=settings.llm_max_output_tokens,
                timeout=settings.llm_timeout_seconds,
            )
        case "gemini":
            from app.llm.gemini_provider import GeminiProvider

            return GeminiProvider(
                model=settings.llm_model,
                api_key=api_key,
                temperature=settings.llm_temperature,
                max_output_tokens=settings.llm_max_output_tokens,
                timeout=settings.llm_timeout_seconds,
            )
