# app/agent.py
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent

from app.config import PSA_PRICE_POLICY, Settings


def build_agent(settings: Settings):
    api_key = (
        settings.llm_api_key.get_secret_value()
        if settings.llm_api_key
        else ""
    )

    provider = settings.llm_provider

    if provider in {"openai", "ollama", "freellmapi"}:
        base_url = settings.llm_base_url

        if not base_url and provider == "ollama":
            base_url = "http://localhost:11434/v1"
        elif not base_url and provider == "freellmapi":
            base_url = "http://localhost:3001/v1"

        model = init_chat_model(
            model=settings.llm_model,
            model_provider="openai",
            api_key=api_key or "ollama" if provider == "ollama" else api_key,
            base_url=base_url,
            temperature=settings.llm_temperature,
            timeout=settings.llm_timeout_seconds,
        )

    elif provider == "anthropic":
        model = init_chat_model(
            model=settings.llm_model,
            model_provider="anthropic",
            api_key=api_key,
            temperature=settings.llm_temperature,
            timeout=settings.llm_timeout_seconds,
            max_tokens=settings.llm_max_output_tokens,
        )

    elif provider == "gemini":
        model = init_chat_model(
            model=settings.llm_model,
            model_provider="google_genai",
            api_key=api_key,
            temperature=settings.llm_temperature,
            timeout=settings.llm_timeout_seconds,
            max_tokens=settings.llm_max_output_tokens,
        )

    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    return create_agent(
        model=model,
        tools=[],
        system_prompt=f"{PSA_PRICE_POLICY} {settings.system_prompt}",
    )