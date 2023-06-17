from datetime import datetime

from news import Item, Source, URL
from .feed import Feed


class Lobsters(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'Lobsters',
            'lob',
            URL('https://lobste.rs/rss'),
        )

    def __repr__(self) -> str:
        return 'Lobsters()'

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            sources=[Source(URL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
