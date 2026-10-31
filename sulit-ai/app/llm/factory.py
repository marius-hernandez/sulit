from langchain.agents import create_agent

from app.config import Settings
from app.llm.base import LLMProvider
from app.tools.psa_prices import get_psa_prices

OLLAMA_DEFAULT_BASE_URL = "http://localhost:11434/v1"
FREELLMAPI_DEFAULT_BASE_URL = "http://localhost:3001/v1"


def create_provider(settings: Settings):
    api_key = settings.llm_api_key.get_secret_value() if settings.llm_api_key else ""

    system_prompt = """
    You are Sulit, a friendly and practical grocery assistant
        for people in the Philippines.
        
        Language rules:
        - Respond in the same language as the user's latest message.
        - If the user speaks Tagalog, respond in natural, conversational Tagalog.
        - If the user speaks English, respond in English.
        - If the user uses Taglish, respond naturally in Taglish.
        - Use simple, everyday Filipino rather than overly formal or
          textbook-style Tagalog.
        - Keep prices in Philippine pesos (₱).
        - Never invent grocery prices. Use provided price data when available.
       You are a grocery assistant.

       When users ask for PSA-reported prices, use the
       get_psa_prices tool when appropriate.

       Never invent prices or reporting periods.
       Explain the reporting period of the returned data.
       """

    return create_agent(
        model=settings.llm_model,
        tools=[get_psa_prices],
        system_prompt=system_prompt,
    )
    return agent

    # # Imports are local so only the selected provider's SDK is loaded.
    # match settings.llm_provider:
    #     case "openai" | "ollama" | "freellmapi":
    #         from app.llm.openai_provider import OpenAIProvider
    #
    #         provider = settings.llm_provider
    #
    #         if provider == "ollama":
    #             default_base_url = OLLAMA_DEFAULT_BASE_URL
    #             effective_api_key = api_key or "ollama"
    #         elif provider == "freellmapi":
    #             default_base_url = FREELLMAPI_DEFAULT_BASE_URL
    #             effective_api_key = api_key
    #         else:
    #             default_base_url = None
    #             effective_api_key = api_key
    #
    #         return OpenAIProvider(
    #             model=settings.llm_model,
    #             api_key=effective_api_key,
    #             base_url=settings.llm_base_url or default_base_url,
    #             temperature=settings.llm_temperature,
    #             timeout=settings.llm_timeout_seconds,
    #         )
    #     case "anthropic":
    #         from app.llm.anthropic_provider import AnthropicProvider
    #
    #         return AnthropicProvider(
    #             model=settings.llm_model,
    #             api_key=api_key,
    #             base_url=settings.llm_base_url,
    #             temperature=settings.llm_temperature,
    #             max_output_tokens=settings.llm_max_output_tokens,
    #             timeout=settings.llm_timeout_seconds,
    #         )
    #     case "gemini":
    #         from app.llm.gemini_provider import GeminiProvider
    #
    #         return GeminiProvider(
    #             model=settings.llm_model,
    #             api_key=api_key,
    #             temperature=settings.llm_temperature,
    #             max_output_tokens=settings.llm_max_output_tokens,
    #             timeout=settings.llm_timeout_seconds,
    #         )
