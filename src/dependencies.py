from typing import Annotated
from fastapi import Depends, HTTPException, Request, Response
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient

from src.core.database import session
from src.utils import decode_jwt
from src.core.config import settings
from src.repositories import UserRepository
from src.models import UserModel


SessionDep = Annotated[AsyncSession, Depends(session)]

def require_refresh_token(request: Request):
	refresh_token = request.cookies.get('refresh')
	if not refresh_token:
		raise HTTPException(status_code=401, detail="Refresh token not found")
	return decode_jwt(refresh_token).get('sub')

async def require_access_token(request: Request, response_api: Response):
    access_token = request.cookies.get('access')
    if not access_token:
        try:
            async with AsyncClient() as client:
                response = await client.get(
                    url=f"{settings.API_URL}{settings.API_PREFIX}/auth/refresh",
                    cookies=request.cookies
                )
                if response.status_code == 401:
                    raise HTTPException(status_code=401, detail="Not authorized")
                access_token = response.cookies.get('access')
                if not access_token:
                    raise HTTPException(status_code=401, detail="Failed to refresh access token")
                response_api.set_cookie(
                    key="access",
                    value=access_token,
                    httponly=True,
                    secure=settings.HTTPS,
                    samesite="lax",
                    max_age=settings.JWT_ACCESS_LIFESPAN_MINUTES * 60
                )
        except Exception as e:
            raise HTTPException(status_code=401, detail="Authentication failed")

    try:
        decoded_token = decode_jwt(access_token)
        return decoded_token.get('sub')
    except jwt.exceptions.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid access token")

async def get_current_user(
	session: SessionDep,
	user_email: str = Depends(require_access_token)
) -> UserModel:
	user = await UserRepository.get_user_by_email(session, user_email)
	if not user:
		raise HTTPException(status_code=401, detail='User not found')
	return user

async def require_superuser(user: UserModel = Depends(get_current_user)):
	if user.is_superuser:
		return user
	raise HTTPException(status_code=401, detail='Not enough permissions')
