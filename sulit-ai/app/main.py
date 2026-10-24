import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.agent import build_agent
from app.config import get_settings
from app.llm import create_provider
from app.routes import router

from typing import Annotated, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field

from langchain.agents import create_agent
from langchain.tools import tool
import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def get_recent_market_price(item:str):
    response=requests.get(f'https://wttr.in/{item}?format=j1')
    return response.json()

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
