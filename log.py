import logging.config

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "std_format": {
            "format": "{asctime}:{levelname}:{name} - {message}:{module}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "std_format",
            "filename": "logger.log",
        }
    },
    "loggers": {
        "route": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "validator": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
        "database": {
            "level": "DEBUG",
            "handlers": ["console"],
        },
    },
}

logging.config.dictConfig(logger_config)

log_route = logging.getLogger("route")
log_validator = logging.getLogger("validator")
log_db = logging.getLogger("database")
