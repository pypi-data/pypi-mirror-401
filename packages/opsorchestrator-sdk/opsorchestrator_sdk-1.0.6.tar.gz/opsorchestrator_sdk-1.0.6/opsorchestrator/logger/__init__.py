"""This script is intended for defining logging format and handling logging cases"""

from logging.config import dictConfig


def initialize_loggers_format():
    """Initialize loggers for the Flask Application"""
    logger = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {
                "format": (
                    "%(levelname)s -- %(asctime)s --"
                    " %(pathname)s:%(lineno)d >  %(message)s "
                ),
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "level": "INFO",
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "backend": {
                "level": "INFO",
                "handlers": ["console"],
            }
        },
    }
    dictConfig(logger)
