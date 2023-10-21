from datetime import datetime

from news import Item, NormalizedURL, Source, URL
from .feed import Feed


class Lobsters(Feed):
    def __init__(self):
        super().__init__('Lobsters', 'lob', URL('https://lobste.rs/rss'))

    def __repr__(self) -> str:
        return 'Lobsters()'

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=NormalizedURL(entry.link),
            title=entry.title,
            sources=[Source(URL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
