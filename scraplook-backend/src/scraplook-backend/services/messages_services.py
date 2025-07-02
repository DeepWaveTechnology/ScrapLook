from models.message import MessageInput
from prisma import Prisma, errors
from prisma.models import Message


async def get_user_messages_sent(
    prisma: Prisma, id_email_address: str
) -> list[Message]:
    return await prisma.message.find_many(
        where={
            "fromId": id_email_address,
            "deleted_by_sender": False
        },
        include={
            "recipients": {
                "include": {"email": True}  # optional: to get email details too
            },
            "fromEmail": True,
        },
        order={
            "sentAt": "asc"
        },
    )


async def get_user_messages_received(
    prisma: Prisma, id_email_address: str
) -> list[Message]:
    return await prisma.message.find_many(
        where={
            "recipients": {
                "some": {
                    "emailId": id_email_address
                }
            },
            "deleted_by_receiver": False
        },
        include={
            "recipients": {
                "include": {"email": True}  # optional: to get email details too
            },
            "fromEmail": True,
        },
        order={"sentAt": "asc"},
    )


async def get_user_message(prisma: Prisma, id_message: str) -> Message:
    return await prisma.message.find_unique_or_raise(
        where={
            "id": id_message
        },
        include={
            "recipients": {
                "include": {
                    "email": True  # optional: to get email details too
                }
            },
            "fromEmail": True
        },
    )


async def send_message(prisma: Prisma, message_info: MessageInput) -> None:
    await prisma.message.create(
        data={
            "subject": message_info.subject,
            "body": message_info.body,
            "fromId": message_info.fromId,
            "recipients": {
                "create": [
                    {
                        "emailId": recipient.emailId,
                        "type": recipient.type
                    } for recipient in message_info.recipients
                ]
            }
        },
    )


async def delete_message(prisma: Prisma, id_email_address: str, id_message: str) -> None:
    #retrieve message information
    try:
        message = await get_user_message(prisma, id_message)
    except errors.RecordNotFoundError:
        #message to delete doesn't exist, so return
        return

    #update message information depending on email address which sent the message
    if message.fromId == id_email_address:
        await prisma.message.update(
            where={
                "id": id_message
            },
            data={
                "deleted_by_sender": True
            }
        )
    else:
        await prisma.message.update(
            where={
                "id": id_message
            },
            data={
                "deleted_by_receiver": True
            }
        )
