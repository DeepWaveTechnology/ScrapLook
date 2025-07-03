from yaml import safe_load
from logging.config import dictConfig


def create_logger(config_file_path) -> None:
    try:
        with open(config_file_path, "r", encoding="utf-8") as fp:
            logger_config = safe_load(fp.read())
    except Exception as e:
        raise Exception(e) from e

    # on créé le logger
    dictConfig(logger_config)
