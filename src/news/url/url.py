from functools import cached_property

from .identity import url_identity


class URL:
    def __init__(self, url: str):
        self.__url = url

    def __eq__(self, other: object) -> bool:
        return isinstance(other, URL) and self.__url == other.__url

    def __hash__(self) -> int:
        return hash(self.__url)

    def __lt__(self, other: 'URL') -> bool:
        return self.__url < other.__url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.__url}')"

    def __str__(self) -> str:
        return self.__url

    @cached_property
    def identity(self) -> str:
        return url_identity(self.__url)
