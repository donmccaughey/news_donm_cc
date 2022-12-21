from datetime import datetime
from feedparser import FeedParserDict, parse

from .item import Item
from .news import News
from .url import URL


class Source:
    def __init__(self, url: URL):
        self.url = url
        self.etag = None
        self.modified = None

    def __repr__(self) -> str:
        return f'Source<{self.url}>'

    def __str__(self) -> str:
        return str(self.url)

    def get(self, now: datetime) -> News:
        d: FeedParserDict = parse(
            str(self.url),
            etag=self.etag,
            modified=self.modified,
            agent='News +https://news.donm.cc',
        )
        if d.status in [200, 302]:
            if 'etag' in d:
                self.etag = d.etag
            if 'modified' in d:
                self.modified = d.modified
            items = [
                Item(
                    url=URL(entry.link),
                    title=entry.title,
                    source=URL(entry.comments),
                    created=now,
                    modified=now,
                )
                for entry in d.entries
            ]
            return News(
                items=items,
                created=now,
                modified=now,
            )
        else:
            # TODO: log error
            return News()
