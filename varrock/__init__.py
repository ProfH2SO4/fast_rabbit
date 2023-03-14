import asyncio
import uvloop


from os.path import isfile
from types import ModuleType

import config
from . import log

from varrock.clients.depositor import depositor_proxy, depositor_client
from varrock.clients.consumer import Consumer

__version__ = "0.0.1"
__started_at__ = "2023-02-25T20:00:00"


def load_config() -> ModuleType:
    """
    Load local config.py.
    If exists config.py in /etc/varrock/ then overrides parameters in local config.py.
    """
    app_config: ModuleType = config
    path: str = "/etc/varrock/config.py"

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


async def start_running():

    version: str = __version__
    started_at: str = __started_at__
    # Load Config
    config_: ModuleType = load_config()
    # Initialize Logger
    print("============ Setting Up Logger ============")
    log.set_up_logger(config_.LOG_CONFIG)
    print("===========Logger, Status: Ready ============")
    # +++++++++++++++DEPOSITOR CLIENT++++++++++++++++++++++++++++++
    log.info("Setting Up Depositor Client")
    print("============ Setting Up Depositor Client ============")
    depositor_proxy.set_up_proxy_object(**parse_namespace("DEPOSITOR_", config_))
    log.info("Depositor Client, Status: Ready")
    print("===========Depositor Client, Status: Ready============")
    # +++++++++++++++DEPOSITOR CLIENT++++++END+++++++++++++++++++++

    consumer_: Consumer = Consumer(**parse_namespace("RABBITMQ_", config_))
    uv_loop: uvloop.Loop = uvloop.new_event_loop()
    asyncio.set_event_loop(uv_loop)

    await consumer_.configure()
    await consumer_.start_to_consume()
