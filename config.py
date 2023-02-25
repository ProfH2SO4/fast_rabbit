LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "FAST_RABBIT" "%(asctime)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "sys_logger6": {
            "level": "INFO",
            "class": "logging.handlers.SysLogHandler",
            "formatter": "default",
            "address": "/dev/log",
            "facility": "local6",
        },
    },
    "loggers": {
        "default": {"level": "INFO", "handlers": ["sys_logger6"], "propagate": True}
    },
    "disable_existing_loggers": False,
}
