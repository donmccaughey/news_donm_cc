import html
from datetime import datetime

from feedparser import FeedParserDict

from feeds.feed import Feed
from news import Item, Source
from news.url import NormalizedURL


class Aggregator(Feed):
    def is_entry_valid(self, entry: dict) -> bool:
        return self.entry_has_keys(entry, ['comments', 'link', 'title'])

    def parse_entry(self, entry: FeedParserDict, now: datetime) -> Item:
        return Item(
            url=NormalizedURL(entry.link),
            title=html.unescape(entry.title),
            sources=[Source(NormalizedURL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
