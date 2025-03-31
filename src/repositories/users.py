from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import UserModel

class UserRepository:
	@classmethod
	async def get_user_by_yandex_id(cls, session: AsyncSession, yandex_id: str):
		try:
			return (await session.execute(
				select(UserModel).where(UserModel.yandex_id == yandex_id)
			)).scalar_one_or_none()
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"Database error: {e}")
		
	@classmethod
	async def create(cls, session: AsyncSession, user_data: dict):
		try:
			user = UserModel(
				yandex_id=user_data['id'],
				email=user_data['default_email'],
				first_name=user_data['first_name'],
				last_name=user_data['last_name'],
				sex=user_data['sex']
			)
			session.add(user)
			await session.commit()
			await session.refresh(user)
			return user
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"Database error: {e}")
		
	@classmethod
	async def get_user_by_email(cls, session: AsyncSession, email: str):
		try:
			return (await session.execute(
				select(UserModel).where(UserModel.email == email)
			)).scalar_one_or_none()
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"Database error: {e}")
		
	@classmethod
	async def update(cls, session: AsyncSession, user: UserModel, update_data: dict) -> UserModel:
		try:
			for key, value in update_data.items():
				setattr(user, key, value)
			session.add(user)
			await session.commit()
			await session.refresh(user)
			return user
		except Exception as e:
			raise HTTPException(status_code=500, detail=f"Database error: {e}")
		