from __future__ import annotations

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.security import safely_decode_token
from app.db.session import get_db
from app.models import User, UserRole
from app.services.user_service import get_user_by_id

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere autenticacion.")

    payload = safely_decode_token(credentials.credentials)
    if payload is None or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalido o expirado.")

    user = get_user_by_id(db, int(payload["sub"]))
    if not user.activo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario inactivo.")
    return user


def require_role(*roles: UserRole):
    def _dependency(user: User = Depends(get_current_user)) -> User:
        if user.rol not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tienes permisos para esta accion.")
        return user

    return _dependency
