from fastapi import APIRouter, Depends, Query
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache
from starlette.responses import JSONResponse
from typing import Annotated
from typing import Literal, Optional

from app.controllers.serializers.response import (
    Response as ResponseSerializer,
    PaginatedResponse,
)
from app.controllers.serializers.chat import (
    MessageCreate as ChatSerializer,
)
from app.services.chat import ChatService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
chat_service = ChatService()

FastAPICache.init(InMemoryBackend())


@router.post(
    "/messages",
    tags=["messages"],
    response_model=ResponseSerializer
)
async def create_chat(
    request: ChatSerializer,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = chat_service.save(request.model_dump())
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )


@router.get(
    "/messages/{session_id}",
    tags=["messages"],
    response_model=PaginatedResponse
)
@cache(expire=30)
async def get_chat(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    limit: Annotated[
        int, Query(ge=1, le=100, description="Número de elementos por página")
    ] = 20,
    offset: Annotated[
        int, Query(ge=0, description="Número de elementos a omitir")
    ] = 0,
    sender: Annotated[
        Optional[Literal["user", "system"]],
        Query(description="Filtra mensajes por remitente: 'user' o 'system'")
    ] = None,
):
    response = chat_service.get_by_session_id(
        session_id, limit, offset, sender
    )
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
