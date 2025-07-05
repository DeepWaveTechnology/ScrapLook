"""
Module that manages app config creation.
"""

from logging import Logger
from typing import Optional
from dotenv import dotenv_values
from pydantic import BaseModel, ValidationError, Field

from config.logger import create_logger, CannotCreateLoggerException, LoggerNotFound

_app_config: Optional["Config"] = None
_DEFAULT_ENCRYPTION_KEY_VALUE = (
    "57699903d1ebdf47ba210a5be9ea4178a5588ba8e7b3cefd70cc3b9e888cc67d"
)


class AppConfigNotCreatedException(Exception):
    """
    Exception raised when app config was not created.
    """

    def __init__(self, message):
        super().__init__(message)


class EnvData(BaseModel):
    """
    Model that stores all environment variables.
    """

    encryption_key: Optional[str] = Field(default=_DEFAULT_ENCRYPTION_KEY_VALUE)
    access_token_duration_minutes: int


class Config(BaseModel):
    """
    Model that stores app configuration.
    """

    logger: Logger
    env_data: EnvData

    class Config:  # pylint: disable=R0903
        """
        Custom config
        """

        arbitrary_types_allowed = True


def get_app_config() -> Config:
    """
    Get app config if already created, otherwise create it and return it.

    Returns:
        Config: app config.
    """
    global _app_config  # pylint: disable=W0603
    default_logger_name = "main_logger"
    path_logger_conf = "logger_config.yaml"
    path_env = ".env"

    # load app config if not loaded
    if not _app_config:

        # retrieve logger
        try:
            logger = create_logger(path_logger_conf, default_logger_name)
        except (CannotCreateLoggerException, LoggerNotFound) as error:
            raise AppConfigNotCreatedException(
                f"Unexpected error while creating logger, error: {error}"
            ) from error

        # retrieve app config
        try:
            env_data = EnvData.model_validate(dotenv_values(path_env))
        except (OSError, ValidationError) as error:
            raise AppConfigNotCreatedException(
                f"Unexpected error while reading env data, error: {error}"
            ) from error

        # create app config
        _app_config = Config(
            logger=logger,
            env_data=env_data,
        )

    return _app_config
