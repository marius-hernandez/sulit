import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from rich.logging import RichHandler

from app.agent import build_agent
from app.config import get_settings
from app.routes import router


logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    # provider = create_provider(settings)
    # app.state.llm_provider = provider
    app.state.agent = build_agent(settings)
    logging.getLogger(__name__).info(
        "LLM provider ready: %s (%s)", settings.llm_provider, settings.llm_model
    )
    try:
        yield
    finally:
        pass
        # await agent.aclose()


app = FastAPI(title="Sulit AI Service", version="0.1.0", lifespan=lifespan)
app.include_router(router)


@app.get("/health", tags=["health"])
async def health() -> dict[str, str]:
    return {"status": "ok"}
