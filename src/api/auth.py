from httpx import AsyncClient
from fastapi import APIRouter, Depends, HTTPException, Query, Response, Request
from fastapi.responses import RedirectResponse

from src.core.config import settings
from src.dependencies import SessionDep
from src.services import AuthService
from src.utils import decode_jwt, encode_access_jwt, encode_refresh_jwt
from src.dependencies import require_refresh_token


router = APIRouter(prefix="/auth", tags=['Authentication'])

@router.get('/yandex')
async def yandex_auth():
	return RedirectResponse(
        f"https://oauth.yandex.ru/authorize?"
        f"response_type=code&client_id={settings.YANDEX_CLIENT_ID}"
        f"&redirect_uri={settings.YANDEX_REDIRECT_URI}"
    )

@router.get('/yandex/callback')
async def yandex_callback(
	session: SessionDep, 
	response: Response, 
	code: str = Query(...)
):
	user_data = await AuthService.get_yandex_userdata(code)
	model_user = await AuthService.get_or_create_user(session, user_data)
	response.set_cookie(
		key="access", 
		value=encode_access_jwt({'sub': model_user.email}), 
		httponly=True, 
		secure=settings.HTTPS,
		samesite='lax',
		max_age=settings.JWT_ACCESS_LIFESPAN_MINUTES * 60
	)
	response.set_cookie(
		key="refresh", 
		value=encode_refresh_jwt({'sub': model_user.email}), 
		httponly=True, 
		secure=settings.HTTPS,
		samesite='lax',
		max_age=settings.JWT_REFRESH_LIFESPAN_DAYS * 24 * 60 * 60
	)
	return {'massage': 'Success'}

@router.get('/refresh')
async def refresh_token(
	response: Response,
	refresh_data: str = Depends(require_refresh_token),
):
	response.set_cookie(
		key="access", 
		value=encode_access_jwt({'sub': refresh_data}), 
		httponly=True, 
		secure=settings.HTTPS,
		samesite='lax',
		max_age=settings.JWT_ACCESS_LIFESPAN_MINUTES * 60
	)
	return {'massage': 'Success'}