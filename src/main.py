import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.api import router
from src.core.database import start_db, dispose_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
	await start_db()
	print('Бд запущена')
	yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

if __name__ == "__main__":
	uvicorn.run(
		'src.main:app',
		reload=True,
		host='0.0.0.0',
		port=8000
	)