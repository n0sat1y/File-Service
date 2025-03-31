from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import SessionDep, require_superuser
from src.models import UserModel


router = APIRouter(prefix="/admin", tags=['Admin'])

@router.get('/users')
async def get_users(
	session: SessionDep,
	user: UserModel = Depends(require_superuser),
) -> list[UserModel]:
	pass