from models.message import MessageInput
from prisma import Prisma
from prisma.models import Message


async def get_user_messages_sent(
    prisma: Prisma, id_email_address: str
) -> list[Message]:
    return await prisma.message.find_many(
        where={
            "fromId": id_email_address,
            "deleted": False
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
            }
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
            "id": id_message,
            "deleted": False
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


async def delete_message(prisma: Prisma, id_message: str) -> None:
    await prisma.message.update(
        where={
            "id": id_message
        },
        data={
            "deleted": True
        }
    )
