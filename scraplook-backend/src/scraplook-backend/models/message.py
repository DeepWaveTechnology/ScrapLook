from pydantic import BaseModel
from typing import List, Optional

class MessageRecipientInput(BaseModel):
    emailId: str
    type: str

class MessageInput(BaseModel):
    subject: Optional[str] = None
    body: str
    fromId: str
    recipients: List[MessageRecipientInput]
