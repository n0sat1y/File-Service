from httpx import AsyncClient
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from fastapi.responses import RedirectResponse

from src.core.config import settings
from src.dependencies import SessionDep


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
	async with AsyncClient() as client:
		response = await client.post(
			"https://oauth.yandex.ru/token",
			data={
				"grant_type": "authorization_code",
				"code": code,
				"client_id": settings.YANDEX_CLIENT_ID,
				"client_secret": settings.YANDEX_CLIENT_SECRET,
				"redirect_uri": settings.YANDEX_REDIRECT_URI
			}
		)
		token_data = response.json()
		user_response = await client.get(
            "https://login.yandex.ru/info",
            params={
                "format": "json",
                "oauth_token": token_data["access_token"]
            }
        )
	return user_response.json()