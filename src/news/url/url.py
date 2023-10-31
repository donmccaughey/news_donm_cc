from .identity import url_identity


class URL:
    def __init__(self, url: str):
        self.__identity: str | None = None
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

    @property
    def identity(self) -> str:
        if not self.__identity:
            self.__identity = url_identity(self.__url)
        return self.__identity
