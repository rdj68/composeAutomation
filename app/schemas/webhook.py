from pydantic import BaseModel

class WebhookResponse(BaseModel):
    message: str