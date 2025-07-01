from pydantic import BaseModel


class EmailAddressInput(BaseModel):
    address: str
    userId: str
