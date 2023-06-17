import html
from datetime import datetime

from news import Item, Source, URL
from .skip_sites import SKIP_SITES
from .feed import Feed


class HackerNews(Feed):
    def __init__(self):
        super().__init__(
            'Hacker News',
            'hn',
            URL('https://news.ycombinator.com/rss'),
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

    def keep_item(self, item: Item) -> bool:
        return item.url.identity not in SKIP_SITES

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=html.unescape(entry.title),
            sources=[Source(URL(entry.comments), self.initials)],
            created=now,
            modified=now,
        )
