from typing import List

from fastapi import APIRouter, Depends, status

from config.prisma_client import get_prisma_instance
from models.email_address import EmailAddressInput
from prisma import Prisma
from prisma.models import Email
from services.email_address_services import get_user_email_addresses, add_email_address, delete_email_address, \
    update_email_address

router = APIRouter(
    prefix="/email_address",
    tags=["email_address"],
    dependencies=[]
)

@router.get("/all", status_code=status.HTTP_200_OK, response_model=List[Email])
async def get_all(user_id: str, prisma: Prisma = Depends(get_prisma_instance)) -> List[Email]:
    return await get_user_email_addresses(prisma, user_id)

@router.post("/", status_code=status.HTTP_200_OK)
async def add_user_email_address(email_info: EmailAddressInput, prisma: Prisma = Depends(get_prisma_instance)):
    return await add_email_address(prisma, email_info)

@router.patch("/{id_email_address}", status_code=status.HTTP_200_OK)
async def update_user_email_address(id_email_address: str, email_info: EmailAddressInput, prisma: Prisma = Depends(get_prisma_instance)):
    return await update_email_address(prisma, id_email_address, email_info)

@router.delete("/{id_email_address}", status_code=status.HTTP_200_OK)
async def delete_user_email_address(id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)):
    return await delete_email_address(prisma, id_email_address)
