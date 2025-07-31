from typing import Optional, Dict

from pydantic import BaseModel, Field


class Response(BaseModel):
    message: str = Field(
        ...,
    )
    data: Optional[Dict] = Field(
        None,
        description="Data for response"
    )


class PaginatedResponse(BaseModel):
    status: str
    data: list
    message: str
    pagination: dict
