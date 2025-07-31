from fastapi import APIRouter

from app.controllers.views import (
    authenticate,
    users,
    chat,
)

urls = APIRouter()


urls.include_router(
    users.router,
    prefix="/api",
)

urls.include_router(
    chat.router,
    prefix="/api",
)

urls.include_router(
    authenticate.router,
)
