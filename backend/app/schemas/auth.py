import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    display_name: str = Field(min_length=1, max_length=100)


class LoginRequest(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: uuid.UUID
    username: str
    email: str
    display_name: str
    avatar: str
    theme: str
    total_xp: int
    level: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    token: str
    user: UserPublic


class PatchMeRequest(BaseModel):
    display_name: str | None = None
    avatar: str | None = None
    theme: Literal["light", "dark"] | None = None
