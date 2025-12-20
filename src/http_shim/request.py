from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True, slots=True)
class Request(Message):
    method: str
    base_url: str
    route: str

    @property
    def start_line(self) -> str:
        return f'{self.method} {self.route} HTTP/1.1'

    @property
    def url(self) -> str:
        return self.base_url + self.route
