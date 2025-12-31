from abc import ABC, abstractmethod
from dataclasses import dataclass

from .body import Body, body_repr
from .headers import Headers, headers_repr


@dataclass(frozen=True, kw_only=True, slots=True)
class Message(ABC):
    headers: Headers
    body: Body | None

    @property
    @abstractmethod
    def start_line(self) -> str: ...

    def __str__(self) -> str:
        return self.to_str('\r\n')

    def to_str(self, line_ending: str) -> str:
        return line_ending.join(
            [
                self.start_line,
                *headers_repr(self.headers),
                '',
                body_repr(self.body),
            ]
        )
