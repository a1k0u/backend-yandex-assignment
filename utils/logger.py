"""
Logger config and loggers for database, validator and routes.
"""

import logging.config

logger_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "app_format": {
            "format": "{asctime}:{levelname}:{name} - {message}:![{module}]!",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "app_format",
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

if __name__ == "__main__":
    log_route.debug("Route logger.")
    log_validator.debug("Validator logger.")
    log_db.debug("DB logger.")
