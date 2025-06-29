from typing import List, Optional
from fastapi import APIRouter, Depends, status

from config.prisma_client import get_prisma_instance
from prisma import Prisma
from prisma.models import User
from services.user_services import get_all_users, get_user_by_id

router = APIRouter(
    prefix="/user",
    tags=["user"],
    dependencies=[]
)

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[User])
async def get_all(prisma: Prisma = Depends(get_prisma_instance)) -> List[User]:
    return await get_all_users(prisma)

@router.get("/{id_user}", status_code=status.HTTP_200_OK, response_model=Optional[User])
async def get_all(id_user: str, prisma: Prisma = Depends(get_prisma_instance)) -> Optional[User]:
    return await get_user_by_id(prisma, id_user)