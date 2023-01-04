from datetime import datetime

from news import Item, Source, URL
from .site import Site


class HackerNews(Site):
    def __init__(self):
        super().__init__(
            URL('https://news.ycombinator.com/rss'),
            'Hacker News', 'hn'
        )

    def __repr__(self) -> str:
        return 'HackerNews()'

    def keep_entry(self, entry) -> bool:
        return self.entry_has_keys(entry, ['link', 'title', 'comments'])

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            source=Source(URL(entry.comments), self.initials),
            created=now,
            modified=now,
        )
