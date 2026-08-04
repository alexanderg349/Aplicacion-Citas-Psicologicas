from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ClinicalHistory(Base):
    __tablename__ = "clinical_histories"

    id: Mapped[int] = mapped_column(primary_key=True)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    motivo_consulta: Mapped[str] = mapped_column(Text, nullable=False)
    antecedentes: Mapped[str | None] = mapped_column(Text, nullable=True)
    diagnostico_inicial: Mapped[str | None] = mapped_column(Text, nullable=True)
    plan_tratamiento: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )

    paciente: Mapped["User"] = relationship(back_populates="historia_clinica")
    evoluciones: Mapped[list["ClinicalEvolution"]] = relationship(back_populates="historia", cascade="all, delete-orphan")
