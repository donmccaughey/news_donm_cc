from datetime import datetime, timezone

from utility.jsontype import JSONDict
from .source import Source
from .url import URL


class Item:
    def __init__(self,
                 url: URL,
                 title: str,
                 sources: list[Source],
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 ):
        self.url = url.clean().rewrite()
        self.title = title
        self.sources = sources

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now

    def __eq__(self, other: 'Item') -> bool:
        return isinstance(other, Item) and self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __repr__(self) -> str:
        return f"Item({repr(self.url)}, '{self.title}', {repr(self.sources)})"

    def __str__(self) -> str:
        return f'"{self.title}" ({self.url})'

    def has_source(self, source: Source) -> bool:
        return source in self.sources

    @property
    def other_sources(self) -> list[Source]:
        return sorted(
            [source for source in self.sources if self.url != source.url],
            key=lambda source: source.site_id,
        )

    @staticmethod
    def decode(encoded: JSONDict) -> 'Item':
        if 'sources' in encoded:
            sources = encoded['sources']
        else:
            sources = [encoded['source']]
        return Item(
            url=URL(encoded['url']),
            title=encoded['title'],
            sources=[Source.decode(source) for source in sources],
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> JSONDict:
        return {
            'url': str(self.url),
            'title': self.title,
            'sources': [source.encode() for source in self.sources],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }
