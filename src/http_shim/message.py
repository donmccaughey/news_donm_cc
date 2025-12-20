from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True, slots=True)
class Message(ABC):
    headers: dict[str, str]
    body: str = ''

    @property
    @abstractmethod
    def start_line(self) -> str: ...

    def __str__(self) -> str:
        return self.to_str('\r\n')

    def to_str(self, line_ending: str) -> str:
        headers = (
            f'{name}: {value}' for name, value in sorted(self.headers.items())
        )
        return line_ending.join([self.start_line, *headers, '', self.body])
