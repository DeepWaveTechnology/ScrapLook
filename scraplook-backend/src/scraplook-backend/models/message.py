from typing import Optional
from pydantic import BaseModel

class MessageRecipientInput(BaseModel):
    emailId: str
    type: str

class MessageInput(BaseModel):
    subject: Optional[str] = None
    body: str
    fromId: str
    recipients: list[MessageRecipientInput]
