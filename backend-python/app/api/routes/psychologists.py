from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas.appointment import AppointmentPublic
from app.schemas.clinical import ClinicalEvolutionCreate, ClinicalHistoryUpsert, PatientHistoryResponse
from app.schemas.user import UserPublic
from app.services.appointment_service import list_psychologist_appointments, update_appointment_status
from app.services.clinical_service import add_clinical_evolution, get_patient_history, upsert_patient_history
from app.services.user_service import get_user_by_id

router = APIRouter(prefix="/psychologists", tags=["psychologists"])


@router.get("/me/agenda", response_model=list[AppointmentPublic])
def agenda(
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
) -> list:
    return list_psychologist_appointments(db, psychologist.id)


@router.get("/me/patients", response_model=list[UserPublic])
def patients(
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
) -> list[UserPublic]:
    appointments = list_psychologist_appointments(db, psychologist.id)
    unique_patients: dict[int, User] = {}
    for appointment in appointments:
        unique_patients[appointment.paciente.id] = appointment.paciente
    return list(unique_patients.values())


@router.get("/me/patients/{patient_id}/history", response_model=PatientHistoryResponse)
def patient_history(
    patient_id: int,
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
) -> PatientHistoryResponse:
    patient = get_user_by_id(db, patient_id)
    appointments = [item for item in list_psychologist_appointments(db, psychologist.id) if item.paciente_id == patient.id]
    history = get_patient_history(db, patient.id)
    return {
        "agenda": appointments,
        "historia": history,
        "evoluciones": history.evoluciones if history else [],
    }


@router.put("/me/patients/{patient_id}/history")
def save_history(
    patient_id: int,
    payload: ClinicalHistoryUpsert,
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
):
    patient = get_user_by_id(db, patient_id)
    return upsert_patient_history(db, psychologist, patient, payload)


@router.post("/me/patients/{patient_id}/evolutions")
def create_evolution(
    patient_id: int,
    payload: ClinicalEvolutionCreate,
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
):
    patient = get_user_by_id(db, patient_id)
    return add_clinical_evolution(db, psychologist, patient, payload)
