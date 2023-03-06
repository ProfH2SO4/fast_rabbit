import aio_pika
from aio_pika import exceptions

from . import log


class Consumer:
    def __init__(
        self, queue_name: str, host: str, port: int, user: str, password: str, **kwargs
    ) -> None:

        self.queue_name: str = queue_name
        self.exchange_name: str = kwargs.get("exchange_name", "default")

        self._host: str = host
        self._port = port
        self._user = user
        self._password = password
        self._vhost = kwargs.get("vhost")
        self._routing_keys: list[str] = kwargs.get("routing_keys")
        self.connection = None
        self.channel = None
        self.exchange = None
        self.queue = None
        self.callback = None

    async def configure(self):
        await self.create_connection()
        await self.create_channel()
        await self.create_exchange()
        await self.queue_declare()
        await self.queue_bind()

    async def create_connection(self):
        """Create connection to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(
                host=self._host, port=self._port
            )
        except exceptions.AMQPConnectionError as e:
            log.error(f"Connection error: {e}")
            raise e from e

    async def create_channel(self):
        """Create channel"""
        self.channel = await self.connection.channel()

    async def create_exchange(self):
        """Create exchange"""
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.TOPIC
        )

    async def queue_declare(self):
        """Declare queue"""
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def queue_bind(self):
        _ = await self.queue.bind(self.exchange, routing_key=self.queue_name)

    async def start_to_consumer(self, callback):
        pass

    def close(self):

        self.channel.stop_consuming()

        self.connection.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
