
import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.dependencies import verify_internal_api_key, get_agent
from app.schemas import ChatRequest, ChatResponse
from app.tools.psa_prices import fetch_psa_data

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

        result = await agent.ainvoke({
            "messages": messages,
        })

        reply = result["messages"][-1].content

        data = await fetch_psa_data({
            "Year": ["6", "7", "8"],
        })

        print(type(data))
        print(list(data.keys()) if isinstance(data, dict) else "Not a dict")

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
