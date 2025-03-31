from pydantic import BaseModel, EmailStr


class UpdateUser(BaseModel):
	first_name: str | None = None
	last_name: str | None = None
	sex: str | None = None

class GetUserChema(UpdateUser):
	id: int
	email: EmailStr

class GetExtendedUserChema(GetUserChema):
	is_superuser: bool
	yandex_id: str