"""
Module that contains all message models.
"""

from typing import Optional
from pydantic import BaseModel


class MessageRecipientInput(BaseModel):
    """
    Model to store message recipients sent to an endpoint.
    """

    emailId: str
    type: str


class MessageInput(BaseModel):
    """
    Model to store message information sent to an endpoint.
    """

    subject: Optional[str] = None
    body: str
    fromId: str
    recipients: list[MessageRecipientInput]
