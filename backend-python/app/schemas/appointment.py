from datetime import datetime

from pydantic import BaseModel, Field

from app.models.enums import AppointmentStatus
from app.schemas.common import ORMModel
from app.schemas.user import UserPublic


class AppointmentCreate(BaseModel):
    psicologo_id: int = Field(gt=0)
    fecha_hora: datetime
    motivo: str = Field(min_length=5, max_length=400)
    observaciones: str | None = Field(default=None, max_length=2000)


class AppointmentStatusUpdate(BaseModel):
    estado: AppointmentStatus


class AppointmentPublic(ORMModel):
    id: int
    fecha_hora: datetime
    motivo: str
    observaciones: str | None = None
    estado: AppointmentStatus
    paciente: UserPublic | None = None
    psicologo: UserPublic | None = None
