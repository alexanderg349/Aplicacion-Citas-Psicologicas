from pydantic import BaseModel

from app.schemas.user import UserPublic


class AdminSummaryResponse(BaseModel):
    totalPacientes: int
    totalPsicologos: int
    totalAdministradores: int
    totalCitas: int
    usuarios: list[UserPublic]
