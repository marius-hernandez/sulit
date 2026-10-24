# app/dependencies.py
import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException, Request, status

from app.config import Settings, get_settings


def get_agent(request: Request):
    return request.app.state.agent


def verify_internal_api_key(
    settings: Annotated[Settings, Depends(get_settings)],
    x_internal_api_key: Annotated[str | None, Header()] = None,
) -> None:
    expected = settings.internal_api_key

    if expected is None:
        return

    if x_internal_api_key is None or not secrets.compare_digest(
        x_internal_api_key, expected.get_secret_value()
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )