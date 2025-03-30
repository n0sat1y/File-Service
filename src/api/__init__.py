from fastapi import APIRouter
from src.core.config import settings

router = APIRouter(prefix=settings.API_PREFIX)


__all__ = [
	'router',
]