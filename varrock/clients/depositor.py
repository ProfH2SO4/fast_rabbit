from aiohttp import ClientSession, ClientTimeout

from varrock.enums import RequestStatus

from varrock.proxy_ import LocalProxy


class AioSession(ClientSession):
    def __init__(self, read_timeout: int, conn_timeout: int, *args, **kwargs):
        super().__init__(
            timeout=ClientTimeout(
                total=read_timeout + conn_timeout,
                sock_read=read_timeout,
                connect=conn_timeout,
            ),
            *args,
            **kwargs
        )


class Depositor:  # simulates a client for storing data
    def __init__(
        self,
        url: str,
        timeout: int,
        max_retries: int,
        read_timeout: int,
        conn_timeout: int,
        *args,
        **kwargs
    ):
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries
        self.aio_session = AioSession(read_timeout, conn_timeout)

    def is_available(self) -> None:
        """
        Ping storage server to check if it is available.
        Try it num_retries times. Raise error if is not available.
        """
        pass

    async def send_user(self, data: dict[str, any]) -> RequestStatus:
        """Send user data to storage server."""
        print(self.url, self.timeout, self.max_retries)
        return RequestStatus.OK

    async def send_measurement(self, data: dict[str, any]) -> RequestStatus:
        """Send measurement data to storage server."""
        pass


depositor_proxy: LocalProxy = LocalProxy(Depositor)
depositor_client: Depositor = depositor_proxy.fake_class_proxy()
