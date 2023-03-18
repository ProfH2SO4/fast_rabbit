from aiohttp import ClientSession, ClientTimeout, ClientResponse
from aiohttp_retry import RetryClient
from varrock.enums import RequestStatus

from varrock.proxy_ import LocalProxy
from varrock import log


class AioSession(ClientSession):
    def __init__(
        self, read_timeout: int, conn_timeout: int, max_retries: int, *args, **kwargs
    ):
        super().__init__(
            timeout=ClientTimeout(
                total=read_timeout + conn_timeout,
                sock_read=read_timeout,
                connect=conn_timeout,
            ),
            *args,
            **kwargs,
        )
        self.max_retries = max_retries
        self.retry_client: RetryClient = RetryClient(self, max_retries=max_retries)

    async def request_async(self, method: str, url: str, **kwargs) -> ClientResponse:
        log.debug(f"Start request to {url} with method {method} and kwargs {kwargs}")
        async with self.retry_client.request(method, url, **kwargs) as response:
            try:
                response_json = await response.json()
                log.debug(f"End Response: {response_json}")
            except ValueError as e:
                log.error(f"Error while parsing response: {e}")
        await self.close()
        return response


class Depositor:  # simulates a client for storing data
    def __init__(
        self,
        url: str,
        timeout: int,
        max_retries: int,
        read_timeout: int,
        conn_timeout: int,
        *args,
        **kwargs,
    ):
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.read_timeout = read_timeout
        self.conn_timeout = conn_timeout

    @property
    def aio_session(self) -> AioSession:
        aio_session = AioSession(self.read_timeout, self.conn_timeout, self.max_retries)
        return aio_session

    async def is_available(self) -> bool:
        """
        Ping storage server to check if it is available.
        Try it num_retries times.
        @return: True if server is available, False otherwise.
        """
        path_: str = "/api/meta/server_ping"
        url: str = self.url + path_
        res: ClientResponse = await self.aio_session.request_async("GET", url)
        return res.status == 200

    async def send_user(self, data: dict[str, any]) -> RequestStatus:
        """Send user data to storage server."""
        return RequestStatus.OK

    async def send_measurement(self, data: dict[str, any]) -> RequestStatus:
        """Send measurement data to storage server."""
        pass


depositor_proxy: LocalProxy = LocalProxy(Depositor)
depositor_client: Depositor = depositor_proxy.fake_class_proxy()
