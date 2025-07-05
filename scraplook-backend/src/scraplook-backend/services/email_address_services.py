"""
Service module to manage users email addresses.
"""

from models.email_address import EmailAddressInput
from prisma import Prisma
from prisma.models import Email


async def get_user_email_addresses(prisma: Prisma, id_user: str) -> list[Email]:
    """
    Retrieve all email addresses of a user in DB.

    Args:
        prisma: DB connection.
        id_user: User ID.

    Returns:
        list[Email]: Email addresses of user.
    """
    return await prisma.email.find_many(
        where={
            "userId": id_user,
        }
    )


async def add_email_address(prisma: Prisma, email_info: EmailAddressInput) -> None:
    """
    Add email address to a user in DB.

    Args:
        prisma: DB connection.
        email_info: Email address information.

    Returns:

    """
    await prisma.email.create(
        data=email_info.model_dump(),
    )


async def update_email_address(
    prisma: Prisma, id_email_address: str, email_info: EmailAddressInput
) -> None:
    """
    Update existing user email address in DB.

    Args:
        prisma: DB connection.
        id_email_address: Email address ID to update.
        email_info: New email address information.

    Returns:

    """
    await prisma.email.update(
        where={
            "id": id_email_address,
        },
        data={"address": email_info.address},
    )


async def delete_email_address(prisma: Prisma, id_email_address: str) -> None:
    """
    Delete existing user email address in DB.

    Args:
        prisma: DB connection.
        id_email_address: Email address ID to delete.

    Returns:

    """
    await prisma.email.delete(where={"id": id_email_address})
