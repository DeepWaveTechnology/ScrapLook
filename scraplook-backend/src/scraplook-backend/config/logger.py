"""
Module that manages app logger creation.
"""

from logging import Logger, getLogger, root
from logging.config import dictConfig
from yaml import safe_load
from yaml.error import YAMLError


class CannotCreateLoggerException(Exception):
    """
    Exception raised when logger cannot be created.
    """

    def __init__(self, message):
        super().__init__(message)


class LoggerNotFound(Exception):
    """
    Exception raised when logger cannot be found.
    """

    def __init__(self, message):
        super().__init__(message)


def create_logger(config_file_path: str, logger_name: str) -> Logger:
    """
    Creater logger from a config file and return logger instance.

    Args:
        config_file_path: Path to the configuration file.
        logger_name: Logger name to return.

    Returns:
        Logger: Logger instance if exists.
    """
    try:
        with open(config_file_path, "r", encoding="utf-8") as fp:
            logger_config = safe_load(fp.read())
    except (OSError, YAMLError) as error:
        raise CannotCreateLoggerException(error) from error

    # create logger
    dictConfig(logger_config)

    # return logger if exists
    if logger_name in root.manager.loggerDict:  # pylint: disable=E1101
        return getLogger(logger_name)

    raise LoggerNotFound(f"Logger {logger_name} not found")
