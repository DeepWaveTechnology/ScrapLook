from logging import Logger, getLogger
from typing import Optional
from dotenv import dotenv_values

from config.logger import create_logger


class Config: #pylint: disable=R0903
    logger: Optional[Logger] = None
    encryption_key: str

def load_app_config(path_logger_conf: str, path_env: str) -> None:
    #create logger
    create_logger(path_logger_conf)
    Config.logger = getLogger("main_logger")

    #load environment variables
    env_values = dotenv_values(path_env)
    encryption_key_index = "encryption_key"
    if encryption_key_index in env_values:
        Config.encryption_key = env_values["encryption_key"]
    else:
        Config.encryption_key = "57699903d1ebdf47ba210a5be9ea4178a5588ba8e7b3cefd70cc3b9e888cc67d"
