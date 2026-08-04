from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.appointment import AppointmentPublic
from app.schemas.common import ORMModel


class ClinicalHistoryUpsert(BaseModel):
    motivo_consulta: str = Field(min_length=5)
    antecedentes: str | None = None
    diagnostico_inicial: str | None = None
    plan_tratamiento: str | None = None


class ClinicalEvolutionCreate(BaseModel):
    cita_id: int | None = Field(default=None, gt=0)
    resumen_sesion: str = Field(min_length=5)
    observaciones: str | None = None
    recomendaciones: str | None = None


class ClinicalHistoryPublic(ORMModel):
    id: int
    motivo_consulta: str
    antecedentes: str | None = None
    diagnostico_inicial: str | None = None
    plan_tratamiento: str | None = None
    updated_at: datetime


class ClinicalEvolutionPublic(ORMModel):
    id: int
    cita_id: int | None = None
    resumen_sesion: str
    observaciones: str | None = None
    recomendaciones: str | None = None
    created_at: datetime


class PatientHistoryResponse(BaseModel):
    historia: ClinicalHistoryPublic | None = None
    evoluciones: list[ClinicalEvolutionPublic]
    agenda: list[AppointmentPublic] = []


class PatientSummaryResponse(BaseModel):
    citas: list[AppointmentPublic]
    historia: PatientHistoryResponse
