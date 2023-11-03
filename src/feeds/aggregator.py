import html
from datetime import datetime

from feeds.feed import Feed
from news import Item, Source
from news.url import NormalizedURL


class Aggregator(Feed):
    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=NormalizedURL(entry.link),
            title=html.unescape(entry.title),
            sources=[Source(NormalizedURL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
