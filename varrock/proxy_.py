import inspect
from typing import TypeVar

T = TypeVar("T")


class LocalProxy(object):
    __slots__ = ["_obj", "__weakref__", "_instance_object", "_was_initiated"]

    def __init__(self, obj: type[T]) -> None:
        self._obj = obj
        self._instance_object = None
        self._was_initiated = False

    def fake_class_proxy(self) -> T:
        """
        1. Find number of required arguments for __init__ method.
        2. Initialize object with None(Fake) values.

        :return: object with fake values
        """
        if self._was_initiated:
            raise RuntimeError("Proxy object was already initiated")
        self._instance_object = self._obj.__new__(self._obj)
        return self._instance_object

    def set_up_proxy_object(self, **kwargs) -> None:
        """Set up proxy object with given kwargs."""
        if self._was_initiated:  # Proxy object was already initiated
            return
        self._instance_object.__init__(**kwargs)
        self._was_initiated = True
