import aio_pika, asyncio, json
from aio_pika import exceptions
from aio_pika import RobustConnection, RobustChannel, RobustQueue, RobustExchange
from aiormq import spec


from varrock import log
from varrock.enums import RequestStatus
from .depositor import storage_client


class Consumer:
    def __init__(
        self, queue_name: str, host: str, port: int, user: str, password: str, **kwargs
    ) -> None:

        self.queue_name: str = queue_name
        self.exchange_name: str = kwargs.get("exchange_name", "default")

        self._host: str = host
        self._port: int = port
        self._user: str = user
        self._password: str = password
        self._vhost: str = kwargs.get("vhost")
        self._routing_keys: list[str] = kwargs.get("routing_keys")
        self.connection: RobustConnection | None = None
        self.channel: RobustChannel | None = None
        self.exchange: RobustExchange | None = None
        self.queue: RobustQueue | None = None
        self.callback = None

    async def configure(self) -> None:
        """
        Configure consumer. Prepare Consumer for consuming messages.
        """
        await self.create_connection()
        await self.create_channel()
        await self.create_exchange()
        await self.queue_declare()
        for routing_key in self._routing_keys:
            await self.queue_bind(routing_key)

    async def create_connection(self) -> None:
        """Create connection to RabbitMQ"""
        try:
            self.connection = await aio_pika.connect_robust(
                host=self._host,
                port=self._port,
                login=self._user,
                password=self._password,
                virtualhost=self._vhost,
            )
        except exceptions.AMQPConnectionError as e:
            log.error(f"Connection error: {e}")
            raise e from e

    async def create_channel(self) -> None:
        """Create channel"""
        self.channel = await self.connection.channel()

    async def create_exchange(self) -> None:
        """Create exchange"""
        self.exchange = await self.channel.declare_exchange(
            self.exchange_name, aio_pika.ExchangeType.TOPIC
        )

    async def queue_declare(self) -> None:
        """Declare queue"""
        self.queue = await self.channel.declare_queue(self.queue_name, durable=True)

    async def queue_bind(self, routing_key: str) -> None:
        """Bind queue to exchange. Expected to receive a type of spec.Queue.BindOk"""
        is_ok: spec.Queue.BindOk = await self.queue.bind(
            self.exchange, routing_key=routing_key
        )
        if not isinstance(is_ok, spec.Queue.BindOk):
            message: str = f"Queue binding failed, expected to receive a type of spec.Queue.BindOk, received: {is_ok}"
            log.error(message)
            raise Exception(message)

    async def process_message(
        self,
        message: aio_pika.abc.AbstractIncomingMessage,
    ) -> None:
        delivery_status: RequestStatus = RequestStatus.OK
        body: dict
        try:
            body = json.loads(message.body)
        except json.JSONDecodeError as e:
            log.warning(f"JSONDecodeError: {e}")
            await message.reject(requeue=False)
            return
        if self.is_users_message(message.routing_key):
            delivery_status = await storage_client.send_user(body)

        if delivery_status == RequestStatus.OK:
            await message.ack()
        else:
            await message.reject(requeue=True)

    async def start_to_consume(self):
        print("Varrock is consuming")
        log.info("Varrock is consuming")
        res = await self.queue.consume(self.process_message)
        try:
            # Wait until terminate
            await asyncio.Future()
        finally:
            await self.connection.close()

    @staticmethod
    def is_users_message(routing_key: str) -> bool:
        """Check if message is a user message"""
        return routing_key.startswith("users.")
