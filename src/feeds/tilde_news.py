from datetime import datetime

from news import Item, Source, URL
from .feed import Feed


class TildeNews(Feed):
    def __init__(self):
        super().__init__('tilde.news', '~n', URL('https://tilde.news/rss'))

    def __repr__(self) -> str:
        return 'TildeNews()'

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            sources=[Source(URL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
