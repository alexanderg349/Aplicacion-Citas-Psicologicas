from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas.appointment import AppointmentCreate, AppointmentPublic
from app.schemas.clinical import PatientSummaryResponse
from app.services.appointment_service import create_appointment_for_patient, list_patient_appointments
from app.services.clinical_service import get_patient_history

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/me/summary", response_model=PatientSummaryResponse)
def my_summary(
    db: Session = Depends(get_db),
    patient: User = Depends(require_role(UserRole.PACIENTE)),
) -> PatientSummaryResponse:
    history = get_patient_history(db, patient.id)
    return {
        "citas": list_patient_appointments(db, patient.id),
        "historia": {
            "historia": history,
            "evoluciones": history.evoluciones if history else [],
            "agenda": [],
        },
    }


@router.post("/me/appointments", response_model=AppointmentPublic, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    patient: User = Depends(require_role(UserRole.PACIENTE)),
) -> AppointmentPublic:
    return create_appointment_for_patient(db, patient, payload)
