from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    email: EmailStr = Field(..., description="Email")
    password_hash: str = Field(..., description="Password hash")


class UserAuthentication(BaseModel):
    email: str = Field(..., description="Email")
    password_hash: str = Field(..., description="Password hash")
