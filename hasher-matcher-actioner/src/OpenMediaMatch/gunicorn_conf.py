import sys
import os
import logging
import datetime

from OpenMediaMatch.utils.formatters import CustomJsonFormatter, GunicornAccessFormatter

accesslog = '-'  # Send access logs to stdout
errorlog = '-'


LOG_FORMAT_JSON = os.environ.get("LOG_FORMAT_JSON", "false") == "true"

if LOG_FORMAT_JSON:
    # Ensure the two named loggers that Gunicorn uses are configured to use a custom
    # JSON formatter.
    logconfig_dict = {
        "version": 1,
        "formatters": {
            "json_request": {
                "()": GunicornAccessFormatter,
            },
            "json_error": {
                "()": CustomJsonFormatter,
            },
        },
        "handlers": {
            "json_request": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json_request"
            },
            "json_error": {
                "class": "logging.StreamHandler",
                "stream": sys.stdout,
                "formatter": "json_error",
            },
        },
        "root": {"level": "INFO", "handlers": []},
        "loggers": {
            "gunicorn.access": {
                "level": "INFO",
                "handlers": ["json_request"],
                "propagate": False,
            },
            "gunicorn.error": {
                "level": "INFO",
                "handlers": ["json_error"],
                "propagate": False,
            },
        },
    }
