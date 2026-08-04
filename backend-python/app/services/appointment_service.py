from __future__ import annotations

from datetime import UTC, datetime

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Appointment, AppointmentStatus, User, UserRole
from app.schemas.appointment import AppointmentCreate
from app.services.notification_service import log_whatsapp_event
from app.services.user_service import get_user_by_id


def _appointment_query():
    return select(Appointment).options(
        joinedload(Appointment.paciente),
        joinedload(Appointment.psicologo),
    )


def list_patient_appointments(db: Session, patient_id: int) -> list[Appointment]:
    return list(
        db.scalars(
            _appointment_query()
            .where(Appointment.paciente_id == patient_id)
            .order_by(Appointment.fecha_hora.asc())
        ).unique().all()
    )


def list_psychologist_appointments(db: Session, psychologist_id: int) -> list[Appointment]:
    return list(
        db.scalars(
            _appointment_query()
            .where(Appointment.psicologo_id == psychologist_id)
            .order_by(Appointment.fecha_hora.asc())
        ).unique().all()
    )


def create_appointment_for_patient(db: Session, patient: User, payload: AppointmentCreate) -> Appointment:
    psychologist = get_user_by_id(db, payload.psicologo_id)
    if psychologist.rol != UserRole.PSICOLOGO:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El profesional seleccionado no es psicologo.")

    if payload.fecha_hora <= datetime.now(UTC):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cita debe programarse en una fecha futura.")

    appointment = Appointment(
        paciente_id=patient.id,
        psicologo_id=psychologist.id,
        fecha_hora=payload.fecha_hora,
        motivo=payload.motivo.strip(),
        observaciones=payload.observaciones.strip() if payload.observaciones else None,
        estado=AppointmentStatus.PROGRAMADA,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    appointment = db.scalar(_appointment_query().where(Appointment.id == appointment.id))
    log_whatsapp_event(db, appointment, "CITA_CREADA")
    return appointment


def update_appointment_status(db: Session, psychologist: User, appointment_id: int, status_value: AppointmentStatus) -> Appointment:
    appointment = db.scalar(_appointment_query().where(Appointment.id == appointment_id))
    if not appointment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cita no encontrada.")
    if appointment.psicologo_id != psychologist.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No puedes modificar citas de otro psicologo.")

    appointment.estado = status_value
    appointment.status_changed_at = datetime.now(UTC)
    db.commit()
    db.refresh(appointment)
    appointment = db.scalar(_appointment_query().where(Appointment.id == appointment.id))
    log_whatsapp_event(db, appointment, "CAMBIO_ESTADO")
    return appointment
