from fastapi import HTTPException
from src.repositories.users import UserRepository

class UserService:
	@classmethod
	async def get_or_create_user(cls, session, user_data):
		user = await UserRepository.get_user_by_yandex_id(session, user_data['id'])
		if not user:
			user = await UserRepository.create(session, user_data)
		return user
	
	@classmethod
	async def get_user_by_id(cls, session, id):
		user = await UserRepository.get_user_by_id(session, id)
		if not user:
			raise HTTPException(status_code=404, detail="User not found")
		return user