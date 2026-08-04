from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ClinicalEvolution(Base):
    __tablename__ = "clinical_evolutions"

    id: Mapped[int] = mapped_column(primary_key=True)
    historia_id: Mapped[int] = mapped_column(ForeignKey("clinical_histories.id"), nullable=False, index=True)
    psicologo_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    cita_id: Mapped[int | None] = mapped_column(ForeignKey("appointments.id"), nullable=True)
    resumen_sesion: Mapped[str] = mapped_column(Text, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    recomendaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False)

    historia: Mapped["ClinicalHistory"] = relationship(back_populates="evoluciones")
    psicologo: Mapped["User"] = relationship(back_populates="evoluciones")
