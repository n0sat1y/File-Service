from typing import Annotated
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import MetaData
from fastapi import Depends

from src.core.config import settings

engine = create_async_engine(
	url=settings.DB_URL,
	# echo=True
)
session_fabric = async_sessionmaker(engine, expire_on_commit=False)

async def session():
	async with session_fabric() as session:
		yield session

class Base(DeclarativeBase):
	metadata = MetaData(naming_convention={
		"all_column_names": lambda constraint, table: "_".join(
			[column.name for column in constraint.columns.values()]
		),
		"ix": "ix__%(table_name)s__%(all_column_names)s",
		"uq": "uq__%(table_name)s__%(all_column_names)s",
		"ck": "ck__%(table_name)s__%(constraint_name)s",
		"fk": "fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s",
		"pk": "pk__%(table_name)s",
	})


async def start_db():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.drop_all)
		await conn.run_sync(Base.metadata.create_all)

async def dispose_engine():
	await engine.dispose()