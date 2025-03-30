from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from src.core.database import Base

class FileModel(Base):
	__tablename__ = 'files'

	id: Mapped[int] = mapped_column(primary_key=True)
	filename: Mapped[str]
	filepath: Mapped[str] = mapped_column(unique=True)
	user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))

	user = relationship('UserModel', back_populates='files')

	def __repr__(self) -> str:
		return f'FileModel(id={self.id}, filename={self.filename})'