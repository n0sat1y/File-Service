from typing import Annotated
from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.core.database import session
from src.utils import decode_jwt
from src.core.config import settings
from src.repositories import AuthRepository
from src.models import UserModel


SessionDep = Annotated[AsyncSession, Depends(session)]

def require_refresh_token(request: Request):
	refresh_token = request.cookies.get('refresh')
	if not refresh_token:
		raise HTTPException(status_code=401, detail="Refresh token not found")
	return decode_jwt(refresh_token).get('sub')

async def require_access_token(request: Request):
	access_token = request.cookies.get('access')
	if not access_token:
		async with AsyncClient() as client:
			response = await client.get(
				url=f"{settings.API_URL}{settings.API_PREFIX}/auth/refresh",
			)
			response.raise_for_status()
			access_token = response.cookies.get('access')
	return decode_jwt(access_token).get('sub')

async def get_current_user(
	session: SessionDep,
	user_email: str = Depends(require_access_token)
) -> UserModel:
	user = await AuthRepository.get_user_by_email(session, user_email)
	if not user:
		raise HTTPException(status_code=401, detail='User not found')
	return user

async def require_superuser(user: UserModel = Depends(get_current_user)):
	if user.is_superuser:
		return user
	raise HTTPException(status_code=401, detail='Not enough permissions')
