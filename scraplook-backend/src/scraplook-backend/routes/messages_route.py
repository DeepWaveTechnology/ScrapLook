"""
Route module to manage messages.
"""

from fastapi import APIRouter, Depends, status, HTTPException
from prisma import Prisma, errors
from prisma.models import Message

from models.message import MessageInput
from services.messages_services import (
    get_user_messages_sent,
    get_user_messages_received,
    get_user_message,
    send_message,
    safe_delete_message,
)
from config.app_config import get_app_config
from config.prisma_client import get_prisma_instance


router = APIRouter(prefix="/messages", tags=["messages"], dependencies=[])
APP_CONFIG = get_app_config()


@router.get("/sent_messages", response_model=list[Message])
async def get_sent_messages(
    id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)
) -> list[Message]:
    """
    Endpoint to retrieve messages sent by an email address.

    Args:
        id_email_address: Email address ID that sent messages.
        prisma: DB connection.

    Returns:
        list[Message]: Messages sent by an email address.
    """
    return await get_user_messages_sent(prisma, id_email_address)


@router.get("/received_messages", response_model=list[Message])
async def get_received_messages(
    id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)
) -> list[Message]:
    """
    Endpoint to get messages received by an email address.

    Args:
        id_email_address: Email address ID that received messages.
        prisma: DB connection.

    Returns:
        list[Message]: Messages received by an email address.
    """
    return await get_user_messages_received(prisma, id_email_address)


@router.get("/{id_message}", response_model=Message)
async def get_message(
    id_message: str, prisma: Prisma = Depends(get_prisma_instance)
) -> Message:
    """
    Endpoint to retrieve message information by ID.

    Args:
        id_message: Message ID to get.
        prisma: DB connection.

    Returns:
        Message: Message information.
    """
    try:
        return await get_user_message(prisma, id_message)
    except errors.RecordNotFoundError as error:
        APP_CONFIG.logger.warning("Message not found: %s", error)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        ) from error


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_mail(
    message_info: MessageInput, prisma: Prisma = Depends(get_prisma_instance)
):
    """
    Endpoint to send a message from an email address.

    Args:
        message_info: Message information to send.
        prisma: DB connection.

    Returns:

    """
    await send_message(prisma, message_info)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_mail(
    id_email_address: str,
    id_message: str,
    prisma: Prisma = Depends(get_prisma_instance),
) -> None:
    """
    Endpoint to delete a message from an email address.

    Args:
        id_email_address: Email address ID where to delete message.
        id_message: Message ID to delete.
        prisma: DB connection.

    Returns:

    """
    await safe_delete_message(prisma, id_email_address, id_message)
