import html
from datetime import datetime

from news import Item, Source, URL
from .site import Site

SKIP_SITES = [
    'english.elpais.com',
    'laphamsquarterly.org',
    'lareviewofbooks.org',
    'lynalden.com',
    'newscientist.com',
    'paulgraham.com',
    'sive.rs',
    'astralcodexten.substack.com',
    'noahpinion.substack.com',
    'theepochtimes.com',
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
            title=html.unescape(entry.title),
            source=Source(URL(entry.comments), self.initials),
            created=now,
            modified=now,
        )
