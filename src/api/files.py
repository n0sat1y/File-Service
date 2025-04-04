from pathlib import Path
from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form

from src.dependencies import get_current_user, validate_file_extension, validate_filename, SessionDep
from src.models import UserModel, FileModel
from src.core.config import settings
from src.repositories import FileRepository
from src.services import FileService
from src.schemas import FileSchema


router = APIRouter(prefix="/files", tags=['Audio Files'])

@router.post('/upload', summary='Upload file', description='Custom filename must consist of 1 to 255 characters and include only Latin letters (a-z, A-Z), Cyrillic letters (а-я, А-Я), numbers (0-9), underscores (_), or hyphens (-). No other characters or empty strings are allowed. If a filename is not provided, it will be retrieved from the uploaded file.')
async def upload_file(
	session: SessionDep,
	user: UserModel = Depends(get_current_user),
	file: UploadFile = Depends(validate_file_extension),
	custom_filename: str = Depends(validate_filename),
) -> FileSchema:
	if not custom_filename:
		custom_filename = '.'.join(file.filename.split('.')[:-1])
	file_path, filename = await FileService.make_file_path(user, file, custom_filename)
	uploaded_file = await FileService.save_file(session, user, file, file_path, filename)
	return FileSchema(
		filename=uploaded_file.filename,
		filepath=uploaded_file.filepath,
	)

@router.get('', summary='Get all files')
async def get_files(
	session: SessionDep,
	user: UserModel = Depends(get_current_user),
) -> list[FileSchema]:
	files = await FileRepository.get_all(session, user.id)
	return [FileSchema(**file.__dict__) for file in files]
