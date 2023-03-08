import inspect
from typing import TypeVar

T = TypeVar("T")


class LocalProxy(object):
    __slots__ = ["_obj", "__weakref__", "_instance_object", "_was_initiated"]

    def __init__(self, obj: T) -> None:
        self._obj = obj
        self._instance_object = None
        self._was_initiated = False

    def fake_class_proxy(self) -> T:
        """
        1. Find number of required arguments for __init__ method.
        2. Initialize object with None(Fake) values.

        :return: object with fake values
        """
        num_of_required_args: int = self._get_num_of_empty_vars()
        self._instance_object = self._obj(*[None for _ in range(num_of_required_args)])
        return self._instance_object

    def set_up_proxy_object(self, **kwargs) -> None:
        """Set up proxy object with given kwargs."""
        for key, value in kwargs.items():
            setattr(self._instance_object, key, value)
        self._was_initiated = True

    def _get_num_of_empty_vars(self) -> int:
        """
        Find out how many variables in __init__ are needed to pass.
        E.g
        __init__(self, a, b="url", c=3) => only one parameter needed.
        The Variables with already assigned values CANNOT be overwritten
        :return: Count of variables needed to make instance of class
        """
        num_of_allowed_params: int = 0
        constructor_parameters = inspect.signature(self._obj.__init__)
        for param in constructor_parameters.parameters.values():
            if param.name == "self" or param.name == "args" or param.name == "kwargs":
                continue
            if param.default is inspect.Parameter.empty:
                num_of_allowed_params += 1
        return num_of_allowed_params
