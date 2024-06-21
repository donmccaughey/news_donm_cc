from datetime import datetime
from typing import cast

from serialize import Encodable, JSONDict, JSONList
from .source import Source
from .url import NormalizedURL


class Item(Encodable):
    def __init__(self,
                 url: NormalizedURL,
                 title: str,
                 sources: list[Source],
                 created: datetime,
                 modified: datetime,
                 ):
        self.url = url
        self.title = title
        self.sources = sources
        self.created = created
        self.modified = modified

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Item) and self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __lt__(self, other: 'Item') -> bool:
        if self.created == other.created:
            return self.url < other.url
        else:
            return self.created > other.created

    def __repr__(self) -> str:
        return f"Item({repr(self.url)}, '{self.title}', {repr(self.sources)})"

    def __str__(self) -> str:
        return f'"{self.title}" ({self.url})'

    @property
    def count(self) -> int:
        return sum(source.count for source in self.sources)

    @property
    def different_sources(self) -> list[Source]:
        return sorted(
            [source for source in self.sources if self.url != source.url],
            key=lambda source: source.site_id,
        )

    def update_from(self, other: 'Item'):
        for other_source in other.sources:
            self.update_from_source(other_source)

    def update_from_source(self, other_source: Source):
        for source in self.sources:
            if source == other_source:
                source.update_from(other_source)
                return
        self.sources.append(other_source)

    @staticmethod
    def decode(encoded: JSONDict | JSONList) -> 'Item':
        encoded = cast(JSONDict, encoded)
        sources = [
            Source.decode(cast(JSONDict, source))
            for source in (cast(JSONList, encoded['sources']))
        ]
        return Item(
            url=NormalizedURL(cast(str, encoded['url'])),
            title=cast(str, encoded['title']),
            sources=sources,
            created=datetime.fromisoformat(cast(str, encoded['created'])),
            modified=datetime.fromisoformat(cast(str, encoded['modified'])),
        )

    def encode(self) -> JSONDict:
        return {
            'url': str(self.url),
            'title': self.title,
            'sources': [source.encode() for source in self.sources],
            'created': self.created.isoformat(),
            'modified': self.modified.isoformat(),
        }
