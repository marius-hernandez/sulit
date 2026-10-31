
import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.dependencies import verify_internal_api_key, get_agent
from app.schemas import ChatRequest, ChatResponse
from app.tools.psa_prices import get_price_context_for_prompt

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/v1",
    dependencies=[Depends(verify_internal_api_key)],
)


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent=Depends(get_agent),
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    try:
        messages = [
            {
                "role": message.role,
                "content": message.content,
            }
            for message in request.messages
        ]

        try:
            price_context = await get_price_context_for_prompt(
                request.messages[-1].content
            )
        except Exception:
            logger.warning(
                "PSA price lookup failed; continuing without price context.",
                exc_info=True,
            )
            price_context = None

        if price_context:
            messages.insert(0, {"role": "system", "content": price_context})

        result = await agent.ainvoke({
            "messages": messages
        })

        reply = result["messages"][-1].content

    except Exception:
        logger.exception("Agent invocation failed")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM request failed.",
        ) from None

    return ChatResponse(
        reply=reply,
        model=settings.llm_model,
    )
