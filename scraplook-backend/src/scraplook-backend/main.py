from contextlib import asynccontextmanager
from logging import getLogger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import email_address_route, messages_route, user_route, seeder_route, auth_route
from config.prisma_client import get_prisma_instance, disconnect_prisma


# manage app lifespan events
@asynccontextmanager
async def lifespan(_: FastAPI):
    # start db connection
    await get_prisma_instance()

    yield

    # disconnect to db
    await disconnect_prisma()


# create server
app = FastAPI(debug=True, lifespan=lifespan)

# update app access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# update logger used
uvicorn_access_logger = getLogger("uvicorn.access")
uvicorn_access_logger.disabled = False

# add app routes
app.include_router(seeder_route.router)
app.include_router(email_address_route.router)
app.include_router(messages_route.router)
app.include_router(user_route.router)
app.include_router(auth_route.router)

