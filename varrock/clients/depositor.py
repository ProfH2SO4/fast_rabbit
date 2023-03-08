from varrock.enums import RequestStatus

from varrock.proxy_ import LocalProxy


class Depositor:  # simulates a client for storing data
    def __init__(self, url: str, timeout: int, max_retries: int, *args, **kwargs):
        self.url = url
        self.timeout = timeout
        self.max_retries = max_retries

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

    async def send_measurement(self, data: dict[str, any]) -> None:
        """Send measurement data to storage server."""
        pass


storage_proxy: LocalProxy = LocalProxy(Depositor)
storage_client: Depositor = storage_proxy.fake_class_proxy()
