from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import session


SessionDep = Annotated[AsyncSession, Depends(session)]