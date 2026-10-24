from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

LLMProviderName = Literal["openai", "anthropic", "gemini", "ollama", "freellmapi"]

DEFAULT_SYSTEM_PROMPT = (
    "You are Sulit, a friendly and practical grocery buddy. "
    "Help users plan grocery lists, stay within budget, and find good-value alternatives. "
    "Keep answers concise and actionable."
)

PSA_PRICE_POLICY = (
    "Only cite PSA-reported prices when PSA price data is supplied in the conversation; "
    "otherwise say that no PSA price is available."
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    llm_provider: LLMProviderName = "openai"
    llm_model: str
    llm_api_key: SecretStr | None = None
    llm_base_url: str | None = None
    llm_temperature: float | None = Field(default=None, ge=0, le=2)
    llm_max_output_tokens: int = Field(default=1024, gt=0)
    llm_timeout_seconds: float = Field(default=60, gt=0)

    system_prompt: str = DEFAULT_SYSTEM_PROMPT
    internal_api_key: SecretStr | None = None

    @model_validator(mode="after")
    def _require_api_key(self) -> "Settings":
        if self.llm_provider != "ollama" and self.llm_api_key is None:
            raise ValueError(f"LLM_API_KEY is required for provider '{self.llm_provider}'.")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore[call-arg]
