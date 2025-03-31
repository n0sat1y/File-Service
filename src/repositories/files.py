from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import FileModel

class FileRepository:
	@classmethod
	async def save_file(cls, session: AsyncSession, filename: str, file_path: str, user_id: int) -> FileModel:
		file = FileModel(filename=filename, filepath=file_path, user_id=user_id)
		session.add(file)
		await session.commit()
		await session.refresh(file)
		return file
	
	@classmethod
	async def get_all(cls, session: AsyncSession, user_id: int) -> list[FileModel]:
		return (await session.execute(
			select(FileModel).where(FileModel.user_id == user_id)
		)).scalars().all()