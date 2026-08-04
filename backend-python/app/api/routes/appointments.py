from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas.appointment import AppointmentPublic, AppointmentStatusUpdate
from app.services.appointment_service import update_appointment_status

router = APIRouter(prefix="/appointments", tags=["appointments"])


@router.patch("/{appointment_id}/status", response_model=AppointmentPublic)
def patch_status(
    appointment_id: int,
    payload: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
    psychologist: User = Depends(require_role(UserRole.PSICOLOGO)),
) -> AppointmentPublic:
    return update_appointment_status(db, psychologist, appointment_id, payload.estado)
