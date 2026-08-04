from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.core.config import get_settings

password_hash = PasswordHash.recommended()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def validate_password_policy(password: str) -> list[str]:
    errors: list[str] = []

    if len(password) < 12:
        errors.append("La contrasena debe tener al menos 12 caracteres.")
    if password.lower() == password:
        errors.append("La contrasena debe incluir al menos una letra mayuscula.")
    if password.upper() == password:
        errors.append("La contrasena debe incluir al menos una letra minuscula.")
    if not any(character.isdigit() for character in password):
        errors.append("La contrasena debe incluir al menos un numero.")
    if not any(not character.isalnum() for character in password):
        errors.append("La contrasena debe incluir al menos un simbolo.")

    return errors


def create_access_token(subject: str, role: str, expires_delta: timedelta | None = None) -> str:
    settings = get_settings()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    payload: dict[str, Any] = {
        "sub": subject,
        "role": role,
        "exp": expire,
        "iat": datetime.now(UTC),
        "iss": settings.app_name,
        "aud": "consultorio-frontend",
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict[str, Any]:
    settings = get_settings()
    return jwt.decode(
        token,
        settings.secret_key,
        algorithms=[settings.algorithm],
        audience="consultorio-frontend",
        issuer=settings.app_name,
    )


def safely_decode_token(token: str) -> dict[str, Any] | None:
    try:
        return decode_token(token)
    except JWTError:
        return None
