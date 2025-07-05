from yaml import safe_load
from yaml.error import YAMLError
from logging import Logger, getLogger, root
from logging.config import dictConfig

class CannotCreateLoggerException(Exception):
    def __init__(self, message):
        super().__init__(message)

class LoggerNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)

def create_logger(config_file_path, logger_name: str) -> Logger:
    try:
        with open(config_file_path, "r", encoding="utf-8") as fp:
            logger_config = safe_load(fp.read())
    except (OSError, YAMLError) as error:
        raise CannotCreateLoggerException(error) from error

    # create logger
    dictConfig(logger_config)

    #return logger if exists
    if logger_name in root.manager.loggerDict:
        return getLogger(logger_name)
    else:
        raise LoggerNotFound(f"Logger {logger_name} not found")
