import asyncio

from fastapi import FastAPI

from os.path import isfile
from types import ModuleType

import config
from . import log
from .consumer import Consumer

__version__ = "0.0.1"
__started_at__ = "2023-02-25T20:00:00"


def load_config() -> ModuleType:
    """
    Load local config.py.
    If exists config.py in /etc/fast_rabbit/ then overrides parameters in local config.py.
    """
    app_config: ModuleType = config
    path: str = "/etc/fast_rabbit/config.py"

    if not isfile(path):
        return app_config
    try:
        with open(path, "rb") as rnf:
            exec(compile(rnf.read(), "config.py", "exec"), app_config.__dict__)
    except OSError as e:
        print(f"File at {path} could not be loaded because of error: {e}")
        raise e from e
    return app_config


def parse_namespace(namespace: str, config: ModuleType) -> dict[str, any]:
    """
    Parse namespace to list.
    """
    parsed: dict[str, any] = {}
    for key, value in config.__dict__.items():
        if namespace in key:
            temp = key.split(namespace)
            parsed[temp[1].lower()] = value
    return parsed


class FastRabbit(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.version: str = __version__
        self.started_at: str = __started_at__
        # Load Config
        self.config: ModuleType = load_config()
        # Initialize Logger
        print("============ Setting Up Logger ============")
        log.set_up_logger(config.LOG_CONFIG)
        print("===========Logger is set up============")
        self.consumer_: Consumer = Consumer(**parse_namespace("RABBITMQ_", self.config))
        asyncio.run(self.start())
        log.info("==== FastRabbit is running ========")
        print("==== FastRabbit is running ========")

    async def start(self):
        await self.consumer_.configure()
        self.consumer_.start()


fast_rabbit = FastRabbit()
