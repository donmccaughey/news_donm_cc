from inspect import getmembers, isfunction

from .method import Method


class Resource:
    @classmethod
    def allow(cls) -> list[str]:
        return [
            getattr(method, 'http_shim.method')
            for method in cls.methods()
        ]

    @classmethod
    def methods(cls) -> list[Method]:
        return [
            func for name, func in getmembers(cls, isfunction)
            if hasattr(func, 'http_shim.method')
        ]
