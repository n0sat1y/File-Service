from pydantic import BaseModel

class FileSchema(BaseModel):
	filename: str
	filepath: str