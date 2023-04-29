import html
from datetime import datetime

from news import Item, Source, URL
from .site import Site

SKIP_SITES = [
    'brave.com',
    'english.elpais.com',
    'europeanreviewofbooks.com',
    'jewishreviewofbooks.com',
    'laphamsquarterly.org',
    'lareviewofbooks.org',
    'lynalden.com',
    'narratively.com',
    'newscientist.com',
    'newstatesman.com',
    'noahpinion.blog',
    'paulgraham.com',
    'quillette.com',
    'reason.com',
    'sive.rs',
    'astralcodexten.substack.com',
    'noahpinion.substack.com',
    'theamericanscholar.org',
    'theepochtimes.com',
]


class HackerNews(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://news.ycombinator.com/rss'),
            'Hacker News', 'hn',
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
