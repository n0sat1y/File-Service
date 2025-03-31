from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import SessionDep, require_superuser, get_current_user
from src.models import UserModel
from src.repositories import UserRepository
from src.schemas import GetExtendedUserChema, UpdateUser
from src.services import UserService


router = APIRouter(prefix="/admin", tags=['Admin'])

@router.get('/users')
async def get_users(
	session: SessionDep,
	user: UserModel = Depends(get_current_user),
) -> list[GetExtendedUserChema]:
	return [GetExtendedUserChema(**user.__dict__) for user in await UserRepository.get_all(session)]

@router.get('/users/{user_id}')
async def get_user_by_id(
	session: SessionDep,
	user_id: int,
	user: UserModel = Depends(get_current_user),
) -> GetExtendedUserChema:
	get_user = await UserService.get_user_by_id(session, user_id)
	return GetExtendedUserChema(**get_user.__dict__)

@router.patch('/users/{user_id}')
async def update_me(
	session: SessionDep,
	user_id: int,
	update_data: UpdateUser,
	user: UserModel = Depends(get_current_user),
) -> GetExtendedUserChema:
	get_user = await UserService.get_user_by_id(session, user_id)
	new_user = await UserRepository.update(
		session=session, 
		user=get_user,
		update_data=update_data.model_dump(exclude_unset=True))
	return GetExtendedUserChema(**new_user.__dict__)

@router.delete('/users/{user_id}')
async def delete_user(
	session: SessionDep,
	user_id: int,
	user: UserModel = Depends(get_current_user),
) -> dict:
	get_user = await UserService.get_user_by_id(session, user_id)
	await UserRepository.delete(session, get_user)
	return {'message': 'Success'}