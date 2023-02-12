from datetime import datetime
from urllib.parse import urlsplit

from news import Item, Source, URL
from .site import Site


SKIP_SITES = [
    'newscientist.com',
    'paulgraham.com',
    'sive.rs',
]


class HackerNews(Site):
    def __init__(self):
        super().__init__(
            URL('https://news.ycombinator.com/rss'),
            'Hacker News', 'hn'
        )

    def __repr__(self) -> str:
        return 'HackerNews()'

    def keep_entry(self, entry) -> bool:
        if not self.entry_has_keys(entry, ['link', 'title', 'comments']):
            return False

        url = URL(entry.link)
        if url.identity in SKIP_SITES:
            return False

        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link).clean(),
            title=entry.title,
            source=Source(URL(entry.comments), self.initials),
            created=now,
            modified=now,
        )
