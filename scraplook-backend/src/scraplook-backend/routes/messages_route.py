from fastapi import APIRouter, Depends, status, HTTPException

from models.message import MessageInput
from services.messages_services import (
    get_user_messages_sent,
    get_user_messages_received,
    get_user_message,
    send_message,
    delete_message,
)
from prisma import Prisma, errors
from prisma.models import Message
from config.prisma_client import get_prisma_instance

router = APIRouter(prefix="/messages", tags=["messages"], dependencies=[])


@router.get("/sent_messages", response_model=list[Message])
async def get_sent_messages(
    id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)
) -> list[Message]:
    return await get_user_messages_sent(prisma, id_email_address)


@router.get("/received_messages", response_model=list[Message])
async def get_received_messages(
    id_email_address: str, prisma: Prisma = Depends(get_prisma_instance)
) -> list[Message]:
    return await get_user_messages_received(prisma, id_email_address)


@router.get("/{id_message}", response_model=Message)
async def get_message(
    id_message: str, prisma: Prisma = Depends(get_prisma_instance)
) -> Message:
    try:
        return await get_user_message(prisma, id_message)
    except errors.RecordNotFoundError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Message not found"
        ) from error


@router.post("/", status_code=status.HTTP_201_CREATED)
async def send_mail(
    message_info: MessageInput, prisma: Prisma = Depends(get_prisma_instance)
):
    await send_message(prisma, message_info)


@router.delete("/", status_code=status.HTTP_200_OK)
async def delete_mail(
    id_email_address: str,
    id_message: str,
    prisma: Prisma = Depends(get_prisma_instance),
) -> None:
    await delete_message(prisma, id_email_address, id_message)
