from dataclasses import dataclass

from .message import Message


@dataclass(frozen=True, kw_only=True, slots=True)
class Response(Message):
    status_code: int
    reason_phrase: str

    @property
    def start_line(self) -> str:
        return f'HTTP/1.1 {self.status_code} {self.reason_phrase}'
