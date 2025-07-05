"""
Main module to manage FastAPI server.
"""

from contextlib import asynccontextmanager
from logging import getLogger
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import (
    email_address_route,
    messages_route,
    user_route,
    seeder_route,
    auth_route,
)
from config.app_config import get_app_config, AppConfigNotCreatedException
from config.prisma_client import get_prisma_instance, disconnect_prisma


# manage app lifespan events
@asynccontextmanager
async def lifespan(_: FastAPI):
    """
    Manage the lifespan of the FastAPI application.
    """
    # load app config
    try:
        app_config = get_app_config()
    except AppConfigNotCreatedException as error:
        raise RuntimeError(error) from error

    app_config.logger.info("Starting application...")

    # start db connection
    await get_prisma_instance()

    yield

    # disconnect to db
    await disconnect_prisma()
    app_config.logger.info("Application stopping ...")


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
