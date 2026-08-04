from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models import Appointment, ClinicalEvolution, ClinicalHistory, User, UserRole
from app.schemas.clinical import ClinicalEvolutionCreate, ClinicalHistoryUpsert


def get_patient_history(db: Session, patient_id: int) -> ClinicalHistory | None:
    return db.scalar(
        select(ClinicalHistory)
        .options(joinedload(ClinicalHistory.evoluciones))
        .where(ClinicalHistory.paciente_id == patient_id)
    )


def upsert_patient_history(db: Session, psychologist: User, patient: User, payload: ClinicalHistoryUpsert) -> ClinicalHistory:
    if psychologist.rol != UserRole.PSICOLOGO:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Solo los psicologos pueden editar historias clinicas.")
    if patient.rol != UserRole.PACIENTE:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La historia clinica solo aplica a pacientes.")

    history = get_patient_history(db, patient.id)
    if history is None:
        history = ClinicalHistory(
            paciente_id=patient.id,
            motivo_consulta=payload.motivo_consulta.strip(),
            antecedentes=payload.antecedentes,
            diagnostico_inicial=payload.diagnostico_inicial,
            plan_tratamiento=payload.plan_tratamiento,
        )
        db.add(history)
    else:
        history.motivo_consulta = payload.motivo_consulta.strip()
        history.antecedentes = payload.antecedentes
        history.diagnostico_inicial = payload.diagnostico_inicial
        history.plan_tratamiento = payload.plan_tratamiento

    db.commit()
    db.refresh(history)
    return history


def add_clinical_evolution(
    db: Session,
    psychologist: User,
    patient: User,
    payload: ClinicalEvolutionCreate,
) -> ClinicalEvolution:
    history = get_patient_history(db, patient.id)
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Primero debes crear la historia clinica.")

    appointment_id = None
    if payload.cita_id:
        appointment = db.get(Appointment, payload.cita_id)
        if not appointment or appointment.paciente_id != patient.id or appointment.psicologo_id != psychologist.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cita asociada no es valida para este caso.")
        appointment_id = appointment.id

    evolution = ClinicalEvolution(
        historia_id=history.id,
        psicologo_id=psychologist.id,
        cita_id=appointment_id,
        resumen_sesion=payload.resumen_sesion.strip(),
        observaciones=payload.observaciones,
        recomendaciones=payload.recomendaciones,
    )
    db.add(evolution)
    db.commit()
    db.refresh(evolution)
    return evolution
