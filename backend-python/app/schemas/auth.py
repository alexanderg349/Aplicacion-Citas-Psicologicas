from pydantic import BaseModel, EmailStr, Field

from app.schemas.user import UserCreate, UserSession


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RegisterRequest(UserCreate):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserSession
