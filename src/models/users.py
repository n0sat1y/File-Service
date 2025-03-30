from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base

class UserModel(Base):
	__tablename__ = 'users'

	id: Mapped[int] = mapped_column(primary_key=True, index=True)
	yandex_id: Mapped[str] = mapped_column(unique=True, nullable=True)
	email: Mapped[str] = mapped_column(unique=True, index=True)
	password: Mapped[str] = mapped_column(nullable=True)
	first_name: Mapped[str] = mapped_column(nullable=True)
	last_name: Mapped[str] = mapped_column(nullable=True)
	sex: Mapped[str] = mapped_column(nullable=True)
	is_superuser: Mapped[bool] = mapped_column(default=False)

	files = relationship('FileModel', back_populates='user', cascade='all, delete')

	def __repr__(self) -> str:
		return f'UserModel(id={self.id}, email={self.email})'