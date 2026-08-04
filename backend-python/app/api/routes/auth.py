from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.rate_limit import rate_limit_auth_requests
from app.db.session import get_db
from app.models import User
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserSession
from app.services.auth_service import authenticate_user, build_user_session, register_patient

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=TokenResponse)
def register(
    payload: RegisterRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    rate_limit_auth_requests(request)
    return register_patient(db, payload)


@router.post("/login", response_model=TokenResponse)
def login(
    payload: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
) -> TokenResponse:
    rate_limit_auth_requests(request)
    return authenticate_user(db, payload)


@router.get("/me", response_model=UserSession)
def me(current_user: User = Depends(get_current_user)) -> UserSession:
    return build_user_session(current_user)
