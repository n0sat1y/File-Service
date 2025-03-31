from httpx import AsyncClient, _exceptions
from fastapi import HTTPException

from src.core.config import settings
from src.repositories import UserRepository


class AuthService:
	@classmethod
	async def get_yandex_userdata(cls, code: str):
		try:
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
				response.raise_for_status()
				token_data = response.json()
				if not token_data:
					raise HTTPException(status_code=400, detail="Empty token data")
				user_response = await client.get(
					"https://login.yandex.ru/info",
					headers={"Authorization": f"OAuth {token_data['access_token']}"}
				)
				user_response.raise_for_status()
				user_data = user_response.json()
				if not user_data:
					raise HTTPException(status_code=400, detail="Empty token data")
				return user_data
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Yandex auth error: {e}")
		
	@classmethod
	async def get_or_create_user(cls, session, user_data):
		user = await UserRepository.get_user_by_yandex_id(session, user_data['id'])
		if not user:
			user = await UserRepository.create_user(session, user_data)
		return user