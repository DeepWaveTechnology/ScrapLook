from fastapi import APIRouter, Depends, status, HTTPException

from config.app_config import Config
from config.prisma_client import get_prisma_instance
from models.email_address import EmailAddressInput
from services.email_address_services import (
    get_user_email_addresses,
    add_email_address,
    delete_email_address,
    update_email_address,
)
from prisma import Prisma, errors
from prisma.models import Email


router = APIRouter(prefix="/email_address", tags=["email_address"], dependencies=[])


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[Email])
async def get_all(
    user_id: str, prisma: Prisma = Depends(get_prisma_instance)
) -> list[Email]:
    return await get_user_email_addresses(prisma, user_id)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user_email_address(
    email_info: EmailAddressInput, prisma: Prisma = Depends(get_prisma_instance)
):
    try:
        await add_email_address(prisma, email_info)
    except errors.UniqueViolationError as error:
        Config.logger.warning("Email address already exists: %s", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email address already exists"
        ) from error


@router.patch("/{id_email_address}", status_code=status.HTTP_200_OK)
async def update_user_email_address(
    id_email_address: str,
    email_info: EmailAddressInput,
    prisma: Prisma = Depends(get_prisma_instance),
):
    return await update_email_address(prisma, id_email_address, email_info)


@router.delete("/{id_email_address}", status_code=status.HTTP_200_OK)
async def delete_user_email_address(
    id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)
):
    return await delete_email_address(prisma, id_email_address)
