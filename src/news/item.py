from datetime import datetime, timezone
from enum import Enum

from .source import Source
from .url import URL


class Age(Enum):
    UNKNOWN = 0
    NEW = 1
    OLD = 2


class Item:
    def __init__(self,
                 url: URL,
                 title: str,
                 source: Source,
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 ):
        self.url = url
        self.title = title
        self.source = source

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now

        self.age = Age.UNKNOWN

    def __eq__(self, other: 'Item') -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f"Item({repr(self.url)}, '{self.title}', {repr(self.source)})"

    def __str__(self) -> str:
        return f'"{self.title}" ({self.url})'

    @staticmethod
    def decode(encoded: dict[str, dict[str, str] | str]) -> 'Item':
        return Item(
            url=URL(encoded['url']),
            title=encoded['title'],
            source=Source.decode(encoded['source']),
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> dict[str, str]:
        return {
            'url': str(self.url),
            'title': self.title,
            'source': self.source.encode(),
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }
