"""
Module that contains email address models.
"""

from pydantic import BaseModel


class EmailAddressInput(BaseModel):
    """
    Model used to store email address information sent to an endpoint.
    """

    address: str
    userId: str
