from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
	#--- SITE ---
	HTTPS: bool = True
	API_URL: str = 'https://hkx7orygw.localto.net/'

	#--- PREFIX ---
	API_PREFIX: str = '/api/v1'

	#--- DB ---
	DB_HOST: str
	DB_PORT: int
	DB_USER: str
	DB_PASS: str
	DB_NAME: str

	@property
	def DB_URL(self) -> str:
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
	
	#--- YANDEX ---
	YANDEX_CLIENT_ID: str
	YANDEX_CLIENT_SECRET: str
	YANDEX_REDIRECT_URI: str

	#--- JWT ---
	SECRET_KEY: str
	JWT_ALGORITHM: str = 'HS256'
	JWT_ACCESS_LIFESPAN_MINUTES: int = 15
	JWT_REFRESH_LIFESPAN_DAYS: int = 10

	#--- AUDIO ---
	AUDIO_PATH: str = "media"
	AUDIO_ALLOWED_TYPES: list = ["mp3", "wav", "flac", "aac", "ogg"]
	AUDIO_FILENAME_PATTERN: str = r"^[a-zA-Z0-9_\-\.]+$"

	model_config = SettingsConfigDict(env_file='.env')

settings = Settings()