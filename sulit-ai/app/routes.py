import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.dependencies import get_provider, verify_internal_api_key
from app.llm import LLMProvider, LLMProviderError
from app.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", dependencies=[Depends(verify_internal_api_key)])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    provider: Annotated[LLMProvider, Depends(get_provider)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> ChatResponse:
    try:
        reply = await provider.generate(request.messages, settings.system_prompt)
    except LLMProviderError:
        logger.exception("LLM provider call failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY, detail="LLM provider request failed."
        ) from None

    return ChatResponse(reply=reply, model=provider.model)
