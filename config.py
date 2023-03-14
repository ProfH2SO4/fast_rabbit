DEPOSITOR_URL = "http://localhost:5432"
DEPOSITOR_TIMEOUT = 10
DEPOSITOR_MAX_RETRIES = 3
DEPOSITOR_READ_TIMEOUT = 10.0
DEPOSITOR_CONN_TIMEOUT = 30.0

RABBITMQ_HOST = "127.0.0.1"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
RABBITMQ_VHOST = "/"
RABBITMQ_QUEUE_NAME = "varrock_queue"
RABBITMQ_EXCHANGE_NAME = "varrock_exchange"
RABBITMQ_HEARTBEAT = 600
RABBITMQ_ROUTING_KEYS = [
    "users.*.created",
    "measurements.*.types.*.started",
    "measurements.*.types.*.finished",
]


LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "VARROCK - %(asctime)s - %(levelname)s - %(message)s",
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
