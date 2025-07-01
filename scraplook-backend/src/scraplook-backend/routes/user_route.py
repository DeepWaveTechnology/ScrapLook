from fastapi import APIRouter, Depends, status, HTTPException

from config.prisma_client import get_prisma_instance
from models.user import UserInput
from prisma import Prisma, errors
from prisma.models import User
from services.user_services import get_all_users, get_user_by_id, add_new_user

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[]
)

@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_all(prisma: Prisma = Depends(get_prisma_instance)) -> list[User]:
    return await get_all_users(prisma)

@router.get("/{id_user}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(id_user: str, prisma: Prisma = Depends(get_prisma_instance)) -> User:
    try:
        return await get_user_by_id(prisma, id_user)
    except errors.RecordNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        ) from error

@router.post("/", status_code=status.HTTP_200_OK, response_model=User)
async def add_user(user_info: UserInput, prisma: Prisma = Depends(get_prisma_instance)) -> User:
    try:
        return await add_new_user(prisma, user_info)
    except errors.UniqueViolationError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User name already exists"
        ) from error
