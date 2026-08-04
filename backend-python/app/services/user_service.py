from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Appointment, User, UserRole
from app.schemas.admin import AdminSummaryResponse
from app.schemas.auth import RegisterRequest
from app.services.auth_service import create_user_and_issue_token


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado.")
    return user


def list_psychologists(db: Session) -> list[User]:
    return list(db.scalars(select(User).where(User.rol == UserRole.PSICOLOGO, User.activo.is_(True)).order_by(User.nombre)).all())


def create_user_from_admin(db: Session, payload: RegisterRequest) -> User:
    token_response = create_user_and_issue_token(db, payload, allow_any_role=True)
    return get_user_by_id(db, token_response.user.id)


def get_admin_summary(db: Session) -> AdminSummaryResponse:
    users = list(db.scalars(select(User).order_by(User.rol, User.nombre, User.apellido)).all())
    total_citas = db.scalar(select(func.count(Appointment.id))) or 0

    return AdminSummaryResponse(
        totalPacientes=sum(1 for user in users if user.rol == UserRole.PACIENTE),
        totalPsicologos=sum(1 for user in users if user.rol == UserRole.PSICOLOGO),
        totalAdministradores=sum(1 for user in users if user.rol == UserRole.ADMINISTRADOR),
        totalCitas=total_citas,
        usuarios=users,
    )
