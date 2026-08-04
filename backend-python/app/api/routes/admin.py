from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import require_role
from app.db.session import get_db
from app.models import User, UserRole
from app.schemas.admin import AdminSummaryResponse
from app.schemas.auth import RegisterRequest
from app.schemas.user import UserPublic
from app.services.user_service import create_user_from_admin, get_admin_summary

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/summary", response_model=AdminSummaryResponse)
def summary(
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMINISTRADOR)),
) -> AdminSummaryResponse:
    return get_admin_summary(db)


@router.post("/users", response_model=UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: RegisterRequest,
    db: Session = Depends(get_db),
    _: User = Depends(require_role(UserRole.ADMINISTRADOR)),
) -> UserPublic:
    return create_user_from_admin(db, payload)
