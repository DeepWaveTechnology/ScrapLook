"""
Database seeder, to initialize database with data.
"""

from random import randint
from fastapi import APIRouter, status, Depends
from prisma import Prisma
from config.prisma_client import get_prisma_instance
from passlib.context import CryptContext

router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    dependencies=[]
)

# Création du contexte bcrypt pour hasher les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.get("/populate", status_code=status.HTTP_201_CREATED)
async def populate_app_data() -> None:
    prisma = await get_prisma_instance()
    await user_seeder(prisma)
    await email_addresses_seeder(prisma)
    await email_messages(prisma)


@router.get("/user", status_code=status.HTTP_201_CREATED)
async def user_seeder(prisma: Prisma = Depends(get_prisma_instance)) -> None:
    users_data = [
        {"name": "AntoninD", "password": "azerty"},
        {"name": "Alice", "password": "alice123"},
        {"name": "Bob", "password": "bob456"},
        {"name": "Charlie", "password": "charlie789"},
        {"name": "Diana", "password": "diana321"},
        {"name": "Ethan", "password": "ethan654"},
    ]

    for user_data in users_data:
        hashed_password = pwd_context.hash(user_data["password"])
        await prisma.user.create(
            data={"name": user_data["name"], "password": hashed_password}
        )


@router.get("/email_addresses", status_code=status.HTTP_201_CREATED)
async def email_addresses_seeder(prisma: Prisma = Depends(get_prisma_instance)) -> None:
    users_data = await prisma.user.find_many()

    for user_data in users_data:
        await prisma.email.create(
            data={"address": f"{user_data.name}.test@gmail.com", "userId": user_data.id}
        )


@router.get("/email_messages", status_code=status.HTTP_201_CREATED)
async def email_messages(prisma: Prisma = Depends(get_prisma_instance)) -> None:
    user_email_addresses = await prisma.email.find_many()

    for _, email_address in enumerate(user_email_addresses):
        await prisma.message.create(
            data={
                "subject": f"Envoi mail par {email_address.address}",
                "body": "Contenu d'un mail test",
                "fromId": email_address.id,
                "recipients": {
                    "create": [
                        {
                            "emailId": user_email_addresses[
                                randint(0, len(user_email_addresses) - 1)
                            ].id,
                            "type": "cc",
                        }
                    ]
                },
            }
        )

@router.get("/reset", status_code=status.HTTP_200_OK)
async def reset_database(prisma: Prisma = Depends(get_prisma_instance)):
    await prisma.messagerecipient.delete_many()
    await prisma.message.delete_many()
    await prisma.email.delete_many()
    await prisma.user.delete_many()
    return {"message": "Database reset successfully"}

