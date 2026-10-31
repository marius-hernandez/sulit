import logging

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import Settings, get_settings
from app.dependencies import get_agent, verify_internal_api_key
from app.schemas import ChatRequest, ChatResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1", dependencies=[Depends(verify_internal_api_key)])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    agent=Depends(get_agent),
    settings: Settings = Depends(get_settings),
) -> ChatResponse:
    messages = [{"role": message.role, "content": message.content} for message in request.messages]
    try:
        result = await agent.ainvoke({"messages": messages})
        reply = result["messages"][-1].content
        if isinstance(reply, list):
            reply = "\n".join(
                part.get("text", "") for part in reply if isinstance(part, dict)
            ).strip()
        if not isinstance(reply, str) or not reply.strip():
            raise ValueError("The model returned an empty response.")
    except Exception:
        logger.exception("Agent invocation failed.")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="LLM request failed.",
        ) from None

    return ChatResponse(reply=reply, model=settings.llm_model)
