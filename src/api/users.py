from fastapi import APIRouter, Depends

from src.dependencies import get_current_user, SessionDep
from src.models import UserModel
from src.schemas import GetUserChema, UpdateUser
from src.repositories.users import UserRepository


router = APIRouter(prefix="/users", tags=['Users'])


@router.get('/me', summary='Get current user data')
async def get_me(user: UserModel = Depends(get_current_user)) -> GetUserChema:
	return GetUserChema(**user.__dict__)

@router.patch('/me', summary='Update current user data')
async def update_me(
	session: SessionDep,
	update_data: UpdateUser,
	user: UserModel = Depends(get_current_user),
) -> GetUserChema:
	new_user = await UserRepository.update(
		session=session, 
		user=user,
		update_data=update_data.model_dump(exclude_unset=True))
	return GetUserChema(**new_user.__dict__)