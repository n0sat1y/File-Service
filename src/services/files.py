from pathlib import Path
from fastapi import HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.models import UserModel
from src.repositories import FileRepository

class FileService:
	@classmethod 
	async def make_file_path(cls, user: UserModel, file: UploadFile, custom_filename: str) -> str:
		file_extension = file.filename.split(".")[-1].lower()
		filename = f"{custom_filename}.{file_extension}"
		path = Path(settings.AUDIO_PATH) / user.email
		path.mkdir(exist_ok=True)
		file_path = path / filename
		if file_path.exists():
			raise HTTPException(status_code=400, detail="File with the same name already exists.")	
		return file_path, filename
	
	@classmethod
	async def save_file(cls, 
		session: AsyncSession, 
		user: UserModel,
		file: UploadFile, 
		file_path: Path, 
		filename: str = None,
	) -> str:
		with open(file_path, "wb") as f:
			f.write(await file.read())
		if not file_path.exists():
			raise HTTPException(status_code=500, detail="Failed to save file.")
		uploaded_file = await FileRepository.save_file(session, filename, str(file_path), user.id)
		if not uploaded_file:
			raise HTTPException(status_code=500, detail="Failed to save file.")
		return uploaded_file