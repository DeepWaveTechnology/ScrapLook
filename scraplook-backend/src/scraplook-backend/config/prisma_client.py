from prisma import Prisma

async def get_prisma_instance() -> Prisma:
    """
    Get prisma instance to manage db.

    :return:
    """
    prisma = Prisma()
    await prisma.connect()

    return prisma
