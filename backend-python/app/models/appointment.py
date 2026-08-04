from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import AppointmentStatus


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    psicologo_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    fecha_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    motivo: Mapped[str] = mapped_column(String(400), nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    estado: Mapped[AppointmentStatus] = mapped_column(Enum(AppointmentStatus), default=AppointmentStatus.PROGRAMADA, nullable=False)
    status_changed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    paciente: Mapped["User"] = relationship(back_populates="patient_appointments", foreign_keys=[paciente_id])
    psicologo: Mapped["User"] = relationship(back_populates="psychologist_appointments", foreign_keys=[psicologo_id])
    whatsapp_logs: Mapped[list["WhatsAppLog"]] = relationship(back_populates="appointment", cascade="all, delete-orphan")
