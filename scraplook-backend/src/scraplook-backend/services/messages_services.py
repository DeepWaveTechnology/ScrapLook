"""
Service module to manage Messages in email addresses.
"""

from models.message import MessageInput
from prisma import Prisma, errors
from prisma.models import Message


async def get_user_messages_sent(
    prisma: Prisma, id_email_address: str
) -> list[Message]:
    """
    Get all user messages sent by given email address in DB.

    Args:
        prisma: DB connection.
        id_email_address: Email address ID to retrieve sent messages.

    Returns:
        list[Message]: Messages sent by given email address.
    """
    return await prisma.message.find_many(
        where={"fromId": id_email_address, "deleted_by_sender": False},
        include={
            "recipients": {
                "include": {"email": True}  # optional: to get email details too
            },
            "fromEmail": True,
        },
        order={"sentAt": "asc"},
    )


async def get_user_messages_received(
    prisma: Prisma, id_email_address: str
) -> list[Message]:
    """
    Get all user messages received by given email address in DB.

    Args:
        prisma: DB connection.
        id_email_address: Email address ID to retrieve received messages.

    Returns:
        list[Message]: Messages received by given email address.
    """
    return await prisma.message.find_many(
        where={
            "recipients": {
                "some": {"emailId": id_email_address, "deletes_message": False}
            },
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
    """
    Get message information in DB.

    Args:
        prisma: DB connection.
        id_message: Message ID to retrieve.

    Returns:
        Message: Message information.
    """
    return await prisma.message.find_unique_or_raise(
        where={"id": id_message},
        include={
            "recipients": {
                "include": {"email": True}  # optional: to get email details too
            },
            "fromEmail": True,
        },
    )


async def send_message(prisma: Prisma, message_info: MessageInput) -> None:
    """
    Add new sent message from given email address to DB.

    Args:
        prisma: DB connection.
        message_info: Message information to add in DB.

    Returns:

    """
    await prisma.message.create(
        data={
            "subject": message_info.subject,
            "body": message_info.body,
            "fromId": message_info.fromId,
            "recipients": {
                "create": [
                    {"emailId": recipient.emailId, "type": recipient.type}
                    for recipient in message_info.recipients
                ]
            },
        },
    )


async def safe_delete_message(
    prisma: Prisma, id_email_address: str, id_message: str
) -> None:
    """
    Delete message from given email address in DB.

    The message is not deleted, it's only not visible for the user who deletes this message.

    Args:
        prisma: DB connection.
        id_email_address: Email address ID that deletes message.
        id_message: Message ID to delete.

    Returns:

    """
    # retrieve message information
    try:
        message = await get_user_message(prisma, id_message)
    except errors.RecordNotFoundError:
        # message to delete doesn't exist, so return
        return

    # update message information depending on email address which sent the message
    if message.fromId == id_email_address:
        await prisma.message.update(
            where={"id": id_message}, data={"deleted_by_sender": True}
        )
    else:
        await prisma.messagerecipient.update(
            where={
                "messageId_emailId": {
                    "messageId": id_message,
                    "emailId": id_email_address,
                }
            },
            data={"deletes_message": True},
        )

    # try to delete this message
    await delete_message(prisma=prisma, id_message=id_message)


async def delete_message(prisma: Prisma, id_message: str) -> None:
    """
    Delete completely message from given email address in DB.

    The message is deleted only if sender and all recipients delete the message.

    Args:
        prisma: DB connection.
        id_message: Message ID to delete.

    Returns:

    """
    # retrieve message information
    try:
        message = await get_user_message(prisma, id_message)
    except errors.RecordNotFoundError:
        # message to delete doesn't exist, so return
        return

    # if all users deleted this message, delete the message on db
    if message.deleted_by_sender and all(
        recipient.deletes_message for recipient in message.recipients
    ):
        await prisma.message.delete(where={"id": message.id})
