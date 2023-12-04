import logging
from logging import config

log_config = {
    "version": 1,
    "root": {
        "handlers": ["console", "info_file", "error_file"],
        "level": "DEBUG"
    },
    "handlers": {
        "console": {
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "DEBUG"
        },
        "info_file": {
            "class": "logging.FileHandler",
            "level": "INFO",
            "formatter": "std_out",
            "filename": "info.log",
            "encoding": "utf8"
        },
        "error_file": {
            "class": "logging.FileHandler",
            "level": "ERROR",
            "formatter": "std_out",
            "filename": "errors.log",
            "encoding": "utf8"
        }
    },
    "formatters": {
        "std_out": {
            "format": "%(asctime)s | %(levelname)s | file name: %(module)s | line: %(lineno)d | message : %(message)s",
            "datefmt": "%d-%m-%Y %I:%M:%S"
        }
    },
}


def get_logger():
    logging.config.dictConfig(log_config)
    logger = logging.getLogger(__name__)
    return logger

