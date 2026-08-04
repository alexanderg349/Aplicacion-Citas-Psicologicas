from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import UserRole


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    apellido: Mapped[str] = mapped_column(String(80), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono: Mapped[str] = mapped_column(String(20), nullable=False)
    rol: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, index=True)
    especialidad: Mapped[str | None] = mapped_column(String(120), nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    patient_appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="paciente",
        foreign_keys="Appointment.paciente_id",
        cascade="all, delete-orphan",
    )
    psychologist_appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="psicologo",
        foreign_keys="Appointment.psicologo_id",
    )
    historia_clinica: Mapped["ClinicalHistory | None"] = relationship(back_populates="paciente", uselist=False)
    evoluciones: Mapped[list["ClinicalEvolution"]] = relationship(back_populates="psicologo")
