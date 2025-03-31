from fastapi import APIRouter
from src.core.config import settings
from src.api.auth import router as auth_router
from src.api.users import router as users_router

router = APIRouter(prefix=settings.API_PREFIX)
router.include_router(auth_router)
router.include_router(users_router)


__all__ = [
	'router',
]