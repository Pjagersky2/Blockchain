"""Module containing the project configuration settings."""
import os

project_path = os.path.sep.join(__file__.split(os.path.sep)[:-1])

logdir = os.path.join(project_path, "logs")
os.makedirs(logdir, exist_ok=True)
logpath = os.path.join(logdir, "blockchain.log")

logger_config = {
    "version": 1,
    "formatters": {
        "standard": {
            "format": "%(message)s"
        },
        "detailed": {
            "format": "%(asctime)s [%(levelname)s] %(message)s"
        }
    },
    "handlers": {
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file": {
            "formatter": "detailed",
            "class": "logging.FileHandler",
            "filename": logpath
        }
    },
    "loggers": {
        "blockchain": {
            "level": "DEBUG",
            "handlers": ["file"]
        }
    }
}
