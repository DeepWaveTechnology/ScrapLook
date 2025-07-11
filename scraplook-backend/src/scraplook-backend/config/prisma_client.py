"""
Module that manages db connection with prisma and singleton method.
"""

from typing import Optional
from prisma import Prisma

_db_connection: Optional[Prisma] = None


async def get_prisma_instance() -> Prisma:
    """
    Return prisma instance if available, otherwise create a new instance and return it.

    Returns:
        Prisma: prisma instance.
    """
    global _db_connection  # pylint: disable=W0603

    if _db_connection is None or not _db_connection.is_connected():
        _db_connection = Prisma()
        await _db_connection.connect()

    return _db_connection


async def disconnect_prisma() -> None:
    """
    Disconnect prisma instance.

    Returns:

    """
    global _db_connection  # pylint: disable=W0603

    if _db_connection and _db_connection.is_connected():
        await _db_connection.disconnect()
        _db_connection = None
