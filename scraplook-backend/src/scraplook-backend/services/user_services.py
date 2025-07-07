"""
Service module to manage users in DB.
"""

from models.user import UserInput
from prisma import Prisma
from prisma.models import User


async def get_all_users(prisma: Prisma) -> list[User]:
    """
    Retrieve all users from DB.

    Args:
        prisma: DB connection.

    Returns:
        list[User]: List of users in DB.
    """
    return await prisma.user.find_many(include={"emails": True})


async def get_user_by_id(prisma: Prisma, id_user: str) -> User:
    """
    Retrieve user by ID in DB.

    Args:
        prisma: DB connection.
        id_user: User ID to retrieve.

    Returns:
        User: User information.
    """
    return await prisma.user.find_unique_or_raise(
        where={"id": id_user}, include={"emails": True}
    )


async def get_user_by_name(prisma: Prisma, user_name: str) -> User:
    """
    Get user by name in DB. If not user was found, raise an exception.

    Args:
        prisma: DB connection.
        user_name: User name to search for.

    Returns:
        User: User object from DB.
    """
    return await prisma.user.find_unique_or_raise(
        where={"name": user_name}, include={"emails": True}
    )


async def add_new_user(prisma: Prisma, user_info: UserInput) -> User:
    """
    Add new user to DB.

    Args:
        prisma: DB connection.
        user_info: User information.

    Returns:
        User: User inserted in DB.
    """
    return await prisma.user.create(data=user_info.model_dump())
