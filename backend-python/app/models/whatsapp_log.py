from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class WhatsAppLog(Base):
    __tablename__ = "whatsapp_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    appointment_id: Mapped[int] = mapped_column(ForeignKey("appointments.id"), nullable=False, index=True)
    telefono_destino: Mapped[str] = mapped_column(String(20), nullable=False)
    evento: Mapped[str] = mapped_column(String(40), nullable=False)
    mensaje: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    appointment: Mapped["Appointment"] = relationship(back_populates="whatsapp_logs")
