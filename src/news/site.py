import logging

from datetime import datetime
from typing import Any

from feedparser import FeedParserDict, parse

from .item import Item
from .news import News
from .source import Source
from .url import URL


log = logging.getLogger(__name__)


class Site:
    def __init__(self, feed_url: URL, name: str, initials: str):
        self.feed_url = feed_url
        self.name = name
        self.initials = initials
        self.etag = None
        self.last_modified = None

    def __repr__(self) -> str:
        return f"Site({repr(self.feed_url)}, '{self.name}', '{self.initials}')"

    def __str__(self) -> str:
        return str(self.name)

    def get(self, now: datetime) -> News:
        d: FeedParserDict = parse(
            str(self.feed_url),
            etag=self.etag,
            modified=self.last_modified,
            agent='News +https://news.donm.cc',
        )
        if d.status in [200, 302]:
            if 'etag' in d:
                self.etag = d.etag
            if 'modified' in d:
                self.last_modified = d.modified
            if self.etag or self.last_modified:
                log.info(f'{self.name}: etag={self.etag}, last_modified={self.last_modified}')
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
            log.warning(f'{self.name} returned status code {d.status}')
            return News()

    def entry_has_keys(self, entry, keys: list[str]) -> bool:
        for key in keys:
            if key not in entry:
                log.warning(f'Entry {repr(entry)} from {self.name} does not have a "{key}" attribute')
                return False
        return True

    def keep_entry(self, entry) -> bool:
        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        raise NotImplementedError()

    def encode(self) -> dict[str, Any]:
        encoded = {
            'feed_url': str(self.feed_url),
            'name': self.name,
            'initials': self.initials,
        }
        if self.etag:
            encoded['etag'] = self.etag
        if self.last_modified:
            encoded['last_modified'] = self.last_modified
        return encoded


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
        if not self.entry_has_keys(entry, ['link', 'title']):
            return False

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
            source=Source(URL(link), self.initials),
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
