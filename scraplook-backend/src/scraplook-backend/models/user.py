from pydantic import BaseModel
from prisma.models import User

class Token(BaseModel):
    access_token: str
    token_type: str

class UserInput(BaseModel):
    name: str
    password: str

class UserOutput(User):
    token: Token
