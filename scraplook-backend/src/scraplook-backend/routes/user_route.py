"""
Route module to manage user.
"""

from fastapi import APIRouter, Depends, status, HTTPException
from prisma import Prisma, errors
from prisma.models import User

from models.user import UserInput
from services.user_services import get_all_users, get_user_by_id, add_new_user
from config.app_config import get_app_config
from config.prisma_client import get_prisma_instance


router = APIRouter(prefix="/user", tags=["user"], dependencies=[])
APP_CONFIG = get_app_config()


@router.get("/all", status_code=status.HTTP_200_OK, response_model=list[User])
async def get_all(prisma: Prisma = Depends(get_prisma_instance)) -> list[User]:
    """
    Endpoint to get all users.

    Args:
        prisma: DB connection.

    Returns:
        list[User]: List of all users.
    """
    return await get_all_users(prisma)


@router.get("/{id_user}", status_code=status.HTTP_200_OK, response_model=User)
async def get_user(id_user: str, prisma: Prisma = Depends(get_prisma_instance)) -> User:
    """
    Endpoint to get a single user given its ID.

    Args:
        id_user: User ID to get.
        prisma: DB connection.

    Returns:
        User: User information.
    """
    try:
        return await get_user_by_id(prisma, id_user)
    except errors.RecordNotFoundError as error:
        APP_CONFIG.logger.warning("User not found: %s", error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from error


@router.post("/", status_code=status.HTTP_200_OK, response_model=User)
async def add_user(
    user_info: UserInput, prisma: Prisma = Depends(get_prisma_instance)
) -> User:
    """
    Endpoint to add a new user.

    Args:
        user_info: User information to add.
        prisma: DB connection.

    Returns:
        User: User added.
    """
    try:
        return await add_new_user(prisma, user_info)
    except errors.UniqueViolationError as error:
        APP_CONFIG.logger.warning("User name already exists: %s", error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User name already exists"
        ) from error
