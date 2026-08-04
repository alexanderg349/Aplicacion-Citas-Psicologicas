from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.models.enums import UserRole
from app.schemas.common import ORMModel


class UserBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=80)
    apellido: str = Field(min_length=2, max_length=80)
    email: EmailStr
    telefono: str = Field(min_length=7, max_length=20)
    especialidad: str | None = Field(default=None, max_length=120)

    @field_validator("telefono")
    @classmethod
    def validate_phone(cls, value: str) -> str:
        normalized = value.replace(" ", "").replace("-", "")
        if not normalized.replace("+", "", 1).isdigit():
            raise ValueError("El telefono solo puede contener numeros, espacios o guiones.")
        return value


class UserCreate(UserBase):
    password: str = Field(min_length=12, max_length=128)
    rol: UserRole = UserRole.PACIENTE


class AdminUserCreate(UserCreate):
    rol: UserRole


class UserPublic(UserBase, ORMModel):
    id: int
    rol: UserRole
    activo: bool
    created_at: datetime | None = None


class UserSession(BaseModel):
    id: int
    nombreCompleto: str
    email: EmailStr
    telefono: str
    rol: UserRole
    especialidad: str | None = None
