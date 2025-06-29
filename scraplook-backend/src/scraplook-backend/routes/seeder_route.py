"""
Database seeder, to initialize database with data.
"""

from fastapi import APIRouter, status, Depends
from config.prisma_client import get_prisma_instance
from prisma import Prisma

router = APIRouter(
    prefix="/seeder",
    tags=["seeder"],
    dependencies=[]
)

@router.get("/user", status_code=status.HTTP_200_OK)
async def user_seeder(prisma: Prisma = Depends(get_prisma_instance)) -> None:
    print(prisma)

    users_data = [
        {'name': 'AntoninD', 'password': 'azerty'},
        {'name': 'Alice', 'password': 'alice123'},
        {'name': 'Bob', 'password': 'bob456'},
        {'name': 'Charlie', 'password': 'charlie789'},
        {'name': 'Diana', 'password': 'diana321'},
        {'name': 'Ethan', 'password': 'ethan654'},
    ]

    for user_data in users_data:
        await prisma.user.create(
            data=user_data
        )

