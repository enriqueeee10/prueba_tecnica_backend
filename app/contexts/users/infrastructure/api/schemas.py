from pydantic import BaseModel, EmailStr
from typing import Optional


class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class CreateUserResponse(BaseModel):
    user_id: str
    message: str


class UserResponse(BaseModel):
    user_id: str
    name: str
    email: str
    is_active: bool


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
