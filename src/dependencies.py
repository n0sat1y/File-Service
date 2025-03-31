import os
import re
from typing import Annotated
from fastapi import Depends, Form, HTTPException, Request, Response, UploadFile, File
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
		raise HTTPException(status_code=401, detail="Not authenticated")
	return decode_jwt(refresh_token).get('sub')

async def require_access_token(request: Request, response_api: Response):
    access_token = request.cookies.get('access')
    if not access_token:
        async with AsyncClient() as client:
            response = await client.post(
                url=f"{settings.API_URL}{settings.API_PREFIX}/auth/refresh",
                cookies=request.cookies
            )
            if response.status_code == 401:
                raise HTTPException(status_code=401, detail=response.json().get('detail'))
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

    try:
        decoded_token = decode_jwt(access_token)
        return decoded_token.get('sub')
    except jwt.exceptions.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid access token: {e}")

async def get_current_user(
	session: SessionDep,
	user_email: str = Depends(require_access_token)
) -> UserModel:
	user = await UserRepository.get_user_by_email(session, user_email)
	if not user:
		raise HTTPException(status_code=401, detail='Current user not found')
	return user

async def require_superuser(user: UserModel = Depends(get_current_user)):
	if user.is_superuser:
		return user
	raise HTTPException(status_code=403, detail='Not enough permissions')

def validate_file_extension(file: UploadFile = File(...)) -> UploadFile:
    file_extension = file.filename.split(".")[-1].lower()
    if file_extension not in settings.AUDIO_ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types are: {', '.join(settings.AUDIO_ALLOWED_TYPES)}"
        )
    return file

def validate_filename(filename: str | None = Form(None)) -> str:
    if not filename:
         return None
    if not re.match(settings.AUDIO_FILENAME_PATTERN, filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid filename. Must match pattern: {settings.AUDIO_FILENAME_PATTERN}"
        )
    return filename

