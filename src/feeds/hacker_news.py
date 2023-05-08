import html
from datetime import datetime

from news import Item, Source, URL
from .skip_sites import SKIP_SITES
from .site import Site


class HackerNews(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://news.ycombinator.com/rss'),
            'Hacker News', 'hn',
        )

    def __repr__(self) -> str:
        return 'HackerNews()'

    def is_entry_valid(self, entry: dict) -> bool:
        return self.entry_has_keys(entry, ['comments', 'link', 'title'])

    def keep_entry(self, entry) -> bool:
        url = URL(entry.link)
        if url.identity in SKIP_SITES:
            return False

        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=html.unescape(entry.title),
            source=Source(URL(entry.comments), self.initials),
            created=now,
            modified=now,
        )
