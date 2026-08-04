from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import create_access_token, hash_password, validate_password_policy, verify_password
from app.models import User, UserRole
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse
from app.schemas.user import UserSession


def build_user_session(user: User) -> UserSession:
    return UserSession(
        id=user.id,
        nombreCompleto=f"{user.nombre} {user.apellido}",
        email=user.email,
        telefono=user.telefono,
        rol=user.rol,
        especialidad=user.especialidad,
    )


def register_patient(db: Session, payload: RegisterRequest) -> TokenResponse:
    if payload.rol != UserRole.PACIENTE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El registro publico solo permite crear pacientes. Los demas roles se crean desde administracion.",
        )
    return create_user_and_issue_token(db, payload, allow_any_role=False)


def create_user_and_issue_token(db: Session, payload: RegisterRequest, allow_any_role: bool) -> TokenResponse:
    if not allow_any_role and payload.rol != UserRole.PACIENTE:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Rol no permitido para este endpoint.")

    existing = db.scalar(select(User).where(User.email == payload.email.lower()))
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El correo ya esta registrado.")

    password_errors = validate_password_policy(payload.password)
    if password_errors:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=password_errors[0])

    if payload.rol == UserRole.PSICOLOGO and not payload.especialidad:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El psicologo debe tener especialidad.")

    user = User(
        nombre=payload.nombre.strip(),
        apellido=payload.apellido.strip(),
        email=payload.email.lower(),
        telefono=payload.telefono.strip(),
        rol=payload.rol,
        especialidad=payload.especialidad.strip() if payload.especialidad else None,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return issue_token_for_user(user)


def authenticate_user(db: Session, payload: LoginRequest) -> TokenResponse:
    settings = get_settings()
    user = db.scalar(select(User).where(User.email == payload.email.lower()))
    generic_error = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales incorrectas.")

    if not user:
        raise generic_error

    if user.locked_until and user.locked_until > datetime.now(UTC):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail="Cuenta bloqueada temporalmente por varios intentos fallidos. Intenta mas tarde.",
        )

    if not user.activo or not verify_password(payload.password, user.password_hash):
        user.failed_login_attempts += 1
        if user.failed_login_attempts >= settings.max_login_failures:
            user.locked_until = datetime.now(UTC) + timedelta(minutes=settings.lock_minutes_after_failures)
            user.failed_login_attempts = 0
        db.commit()
        raise generic_error

    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()
    return issue_token_for_user(user)


def issue_token_for_user(user: User) -> TokenResponse:
    settings = get_settings()
    token = create_access_token(subject=str(user.id), role=user.rol.value)
    return TokenResponse(
        access_token=token,
        expires_in=settings.access_token_expire_minutes * 60,
        user=build_user_session(user),
    )
