from pydantic import BaseModel

class RestartResponse(BaseModel):
    message: str
    success: bool

class RestartReq(BaseModel):
	secret: str