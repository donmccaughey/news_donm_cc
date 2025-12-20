from typing import Callable, Concatenate

from .request import Request
from .response import Response


type Method[T, **P] = Callable[Concatenate[T, Request, P], Response]


def method[T, **P](func: Method[T, P]) -> Method[T, P]:
    def wrapper(
            self: T, request: Request, *args: P.args, **kwargs: P.kwargs
    ) -> Response:
        return func(self, request, *args, **kwargs)
    wrapper.__name__ = func.__name__
    setattr(wrapper, 'http_shim.method', func.__name__.upper())
    return wrapper
