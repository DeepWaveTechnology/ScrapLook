from models.user import UserInput
from prisma import Prisma
from prisma.models import User


async def get_all_users(prisma: Prisma) -> list[User]:
    return await prisma.user.find_many(include={"emails": True})


async def get_user_by_id(prisma: Prisma, id_user: str) -> User:
    return await prisma.user.find_unique_or_raise(
        where={"id": id_user}, include={"emails": True}
    )

async def get_user_by_name(prisma: Prisma, id_name: str) -> User:
    return await prisma.user.find_unique_or_raise(
        where={
            "name": id_name
        },
        include={
            "emails": True
        }
    )

async def add_new_user(prisma: Prisma, user_info: UserInput) -> User:
    return await prisma.user.create(data=user_info.model_dump())
