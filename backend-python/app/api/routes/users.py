from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models import User
from app.schemas.user import UserPublic
from app.services.user_service import list_psychologists

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/psychologists", response_model=list[UserPublic])
def psychologists(
    db: Session = Depends(get_db),
    _: User = Depends(get_current_user),
) -> list[UserPublic]:
    return list_psychologists(db)
