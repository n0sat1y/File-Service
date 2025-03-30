import jwt
from datetime import datetime, timedelta, timezone
from src.core.config import settings


def encode_jwt(
		payload: dict, 
		type: str, 
		timedelta_minutes: int = 0, 
		timedelta_days: int = 0,
		key: str = settings.SECRET_KEY,
		algorithm: str = settings.JWT_ALGORITHM,
	):
	payload['iat'] = datetime.now(timezone.utc)
	payload['exp'] = datetime.now(timezone.utc) + timedelta(minutes=timedelta_minutes, days=timedelta_days)
	payload['type'] = type
	
	token = jwt.encode(payload, key, algorithm)
	return token

def encode_access_jwt(
		payload: dict, 
		token_lifetime_minutes: int = settings.JWT_ACCESS_LIFESPAN_MINUTES
	):
	return encode_jwt(payload, 'access', timedelta_minutes=token_lifetime_minutes)

def encode_refresh_jwt(
		payload: dict,
		token_lifetime_days: int = settings.JWT_REFRESH_LIFESPAN_DAYS
	):
	return encode_jwt(payload, 'refresh', timedelta_days=token_lifetime_days)

def decode_jwt(
		token: str,
		key: str = settings.SECRET_KEY,
		algorithm: str = settings.JWT_ALGORITHM
		):
	data = jwt.decode(token, key, algorithms=[algorithm])
	return data