"""
Module that contains user models.
"""

from pydantic import BaseModel
from prisma.models import User


class Token(BaseModel):
    """
    Model to store user token information.
    """

    access_token: str
    token_type: str


class UserInput(BaseModel):
    """
    Model to store user information sent to an endpoint.
    """

    name: str
    password: str


class UserOutput(User):
    """
    Model to store user information sent by an endpoint.
    """

    token: Token
