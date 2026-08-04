from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import select

from app.core.config import get_settings
from app.core.security import hash_password
from app.db.session import SessionLocal
from app.models import Appointment, AppointmentStatus, ClinicalHistory, User, UserRole


def seed_demo_data() -> None:
    settings = get_settings()
    if not settings.seed_demo_data:
        return

    with SessionLocal() as db:
        if db.scalar(select(User.id).limit(1)):
            return

        admin = User(
            nombre="Administrador",
            apellido="Principal",
            email="admin@psicologia.com",
            telefono="3000000001",
            rol=UserRole.ADMINISTRADOR,
            password_hash=hash_password("Admin123*Seguro"),
        )
        psychologist = User(
            nombre="Laura",
            apellido="Ramirez",
            email="psicologo@psicologia.com",
            telefono="3000000002",
            rol=UserRole.PSICOLOGO,
            especialidad="Terapia cognitivo conductual",
            password_hash=hash_password("Psico123*Seguro"),
        )
        patient = User(
            nombre="Carlos",
            apellido="Gomez",
            email="paciente@psicologia.com",
            telefono="3000000003",
            rol=UserRole.PACIENTE,
            password_hash=hash_password("Paciente123*Seguro"),
        )
        db.add_all([admin, psychologist, patient])
        db.commit()
        db.refresh(psychologist)
        db.refresh(patient)

        history = ClinicalHistory(
            paciente_id=patient.id,
            motivo_consulta="Ansiedad laboral y dificultades para dormir.",
            antecedentes="No registra hospitalizaciones. Reporta episodios previos de estres.",
            diagnostico_inicial="Sintomas compatibles con ansiedad moderada.",
            plan_tratamiento="Sesiones semanales y tecnicas de respiracion.",
        )
        db.add(history)

        db.add_all(
            [
                Appointment(
                    paciente_id=patient.id,
                    psicologo_id=psychologist.id,
                    fecha_hora=datetime.now(UTC) - timedelta(days=3),
                    motivo="Valoracion inicial",
                    estado=AppointmentStatus.COMPLETADA,
                    observaciones="Se registro informacion base para la historia clinica.",
                ),
                Appointment(
                    paciente_id=patient.id,
                    psicologo_id=psychologist.id,
                    fecha_hora=datetime.now(UTC) + timedelta(days=6),
                    motivo="Seguimiento terapeutico",
                    estado=AppointmentStatus.PROGRAMADA,
                    observaciones="Sesion virtual solicitada por el paciente.",
                ),
            ]
        )
        db.commit()
