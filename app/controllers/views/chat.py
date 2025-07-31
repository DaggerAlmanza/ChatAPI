from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse
from typing import Annotated

from app.controllers.serializers.response import (
    Response as ResponseSerializer,
)
from app.controllers.serializers.chat import (
    MessageCreate as ChatSerializer,
)
from app.services.chat import ChatService
from app.controllers.views.authenticate import get_current_user


router = APIRouter()
chat_service = ChatService()


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
    response_model=ResponseSerializer
)
async def get_chat(
    session_id: str,
    current_user: Annotated[dict, Depends(get_current_user)]
):
    response = chat_service.get_by_session_id(session_id)
    return JSONResponse(
        status_code=response.pop("status_code"),
        content=response
    )
