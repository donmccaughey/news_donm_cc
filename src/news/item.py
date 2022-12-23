from datetime import datetime, timezone

from .url import URL


class Item:
    def __init__(self,
                 url: URL,
                 title: str,
                 source: URL,
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 ):
        self.url = url
        self.title = title
        self.source = source

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now

    def __eq__(self, other: 'Item') -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f"Item(URL('{self.url}'), '{self.title}', URL('{self.source}'))"

    def __str__(self) -> str:
        return f'"{self.title}" ({self.url})'

    @staticmethod
    def decode(encoded: dict[str, str]) -> 'Item':
        return Item(
            url=URL(encoded['url']),
            title=encoded['title'],
            source=URL(encoded['source']),
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> dict[str, str]:
        return {
            'url': str(self.url),
            'title': self.title,
            'source': str(self.source),
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }
