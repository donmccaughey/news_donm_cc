from datetime import datetime
from feedparser import FeedParserDict, parse

from .item import Item
from .news import News
from .url import URL


class Site:
    def __init__(self, url: URL, name: str, initials: str):
        self.url = url
        self.name = name
        self.initials = initials
        self.etag = None
        self.modified = None

    def __repr__(self) -> str:
        return f"Site(URL('{self.url}'), '{self.name}', '{self.initials}')"

    def __str__(self) -> str:
        return str(self.name)

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
                self.parse_entry(entry, now) for entry in d.entries
                if self.keep_entry(entry)
            ]
            return News(
                items=items,
                created=now,
                modified=now,
            )
        else:
            # TODO: log error
            return News()

    def keep_entry(self, entry) -> bool:
        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        raise NotImplementedError()


def first_link_with_rel(links, rel: str):
    for link in links:
        if link['rel'] == rel:
            return link.href
    return None


class DaringFireball(Site):
    def __init__(self):
        super().__init__(
            URL('https://daringfireball.net/feeds/main'),
            'Daring Fireball', 'df'
        )

    def __repr__(self) -> str:
        return 'DaringFireball()'

    def keep_entry(self, entry) -> bool:
        related = first_link_with_rel(entry.links, 'related')
        if related and related.startswith('https://daringfireball.net/feeds/sponsors/'):
            return False
        else:
            return True

    def parse_entry(self, entry, now: datetime) -> Item:
        related = first_link_with_rel(entry.links, 'related')
        alternate = first_link_with_rel(entry.links, 'alternate')
        link = related or alternate or entry.link

        return Item(
            url=URL(link),
            title=entry.title,
            source=URL(link),
            created=now,
            modified=now,
        )


class HackerNews(Site):
    def __init__(self):
        super().__init__(
            URL('https://news.ycombinator.com/rss'),
            'Hacker News', 'hn'
        )

    def __repr__(self) -> str:
        return 'HackerNews()'

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            source=URL(entry.comments),
            created=now,
            modified=now,
        )
