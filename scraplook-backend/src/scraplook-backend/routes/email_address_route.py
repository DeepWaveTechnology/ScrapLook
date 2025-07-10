"""
Route module to manage email addresses
"""

from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException

from prisma import Prisma, errors
from prisma.models import Email

from models.user import UserOutput
from models.email_address import EmailAddressInput
from routes.auth_route import get_current_user
from services.email_address_services import (
    get_user_email_addresses,
    add_email_address,
    delete_email_address,
    update_email_address,
    get_email_address_information,
)
from config.app_config import get_app_config
from config.prisma_client import get_prisma_instance

router = APIRouter(prefix="/email_address", tags=["email_address"], dependencies=[])
APP_CONFIG = get_app_config()


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[Email])
async def get_all(
    user: Annotated[UserOutput, Depends(get_current_user)],
    user_id: str,
    prisma: Prisma = Depends(get_prisma_instance),
) -> list[Email]:
    """
    Endpoint to get all email addresses for a given user.

    Args:
        user_id: User ID.
        prisma: DB connection.

    Returns:
        list[Email]: Email addresses of the user.
    """
    return await get_user_email_addresses(prisma, user_id)


@router.get("/{id_email_address}", status_code=status.HTTP_200_OK, response_model=Email)
async def get_one(
    user: Annotated[UserOutput, Depends(get_current_user)],
    id_email_address: str,
    prisma: Prisma = Depends(get_prisma_instance),
) -> Email:
    """
    Endpoint to get an email.

    Args:
        id_email_address: Email address ID.
        prisma: DB connection.

    Returns:
        Email: Email address of the user.
    """
    try:
        return await get_email_address_information(prisma, id_email_address)
    except errors.RecordNotFoundError as error:
        APP_CONFIG.logger.warning("Email address not found: %s", error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email address not found"
        ) from error


@router.post("/", status_code=status.HTTP_201_CREATED)
async def add_user_email_address(
    user: Annotated[UserOutput, Depends(get_current_user)],
    email_info: EmailAddressInput,
    prisma: Prisma = Depends(get_prisma_instance),
):
    """
    Endpoint to add a new email address to a given user.

    Args:
        email_info: Email address information to add.
        prisma: DB connection.

    Returns:

    """
    try:
        await add_email_address(prisma, email_info)
    except errors.UniqueViolationError as error:
        APP_CONFIG.logger.warning("Email address already exists: %s", error)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email address already exists"
        ) from error


@router.patch("/{id_email_address}", status_code=status.HTTP_200_OK)
async def update_user_email_address(
    user: Annotated[UserOutput, Depends(get_current_user)],
    id_email_address: str,
    email_info: EmailAddressInput,
    prisma: Prisma = Depends(get_prisma_instance),
):
    """
    Endpoint to update a user email address.

    Args:
        id_email_address: Email address ID to update.
        email_info: New email address information.
        prisma: DB connection.

    Returns:

    """
    return await update_email_address(prisma, id_email_address, email_info)


@router.delete("/{id_email_address}", status_code=status.HTTP_200_OK)
async def delete_user_email_address(
    user: Annotated[UserOutput, Depends(get_current_user)],
    id_email_address: str,
    prisma: Prisma = Depends(get_prisma_instance),
):
    """
    Endpoint to delete a user email address.

    Args:
        id_email_address: Email address ID to delete.
        prisma: DB connection.

    Returns:

    """
    return await delete_email_address(prisma, id_email_address)
