import calendar
import logging
from datetime import datetime, timezone

from feedparser import FeedParserDict, parse

from news import LIFETIME, Item, Source, URL
from utility.jsontype import JSONDict


log = logging.getLogger(__name__)


class Feed:
    def __init__(self,
                 options: dict,
                 name: str,
                 initials: str,
                 feed_url: URL,
                 etag: str | None = None,
                 last_modified: str | None = None,
                 ):
        self.options = options
        self.feed_url = feed_url
        self.name = name
        self.initials = initials
        self.etag = etag
        self.last_modified = last_modified

    def __eq__(self, other: 'Feed') -> bool:
        return isinstance(other, Feed) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Feed({repr(self.options)}, '{self.name}', '{self.initials}', {repr(self.feed_url)})"

    def __str__(self) -> str:
        return str(self.name)

    def entry_has_keys(self, entry: dict, keys: list[str]) -> bool:
        for key in keys:
            if key not in entry:
                log.warning(f'Entry {repr(entry)} from {self.name} does not have a "{key}" attribute')
                return False
        return True

    def get_items(self, now: datetime) -> list[Item]:
        d: FeedParserDict = parse(
            str(self.feed_url),
            etag=self.etag,
            modified=self.last_modified,
            agent='News +https://news.donm.cc',
        )
        if 'status' not in d:
            log.warning(f'{self.name} failed without status code')
            return []
        if d.status in [200, 302]:  # OK, Found
            if 'etag' in d:
                self.etag = d.etag
            if 'modified' in d:
                self.last_modified = d.modified
            return self.parse_entries(d.entries, now)
        elif d.status in [301, 308]:  # Moved Permanently, Permanent Redirect
            location = f': {d.href}' if 'href' in d else ''
            log.warning(f'{self.name} returned status code {d.status}{location}')
            return []
        elif d.status == 304:  # Not Modified
            return []
        else:
            log.warning(f'{self.name} returned status code {d.status}')
            return []

    def is_entry_recent(self, entry: dict, now: datetime) -> bool:
        time_tuple = (
                entry.get('published_parsed')
                or entry.get('updated_parsed')
                or entry.get('created_parsed')
                or None
        )
        if time_tuple:
            timestamp = calendar.timegm(time_tuple)
            published = datetime.fromtimestamp(timestamp, timezone.utc)
            return (now - published) < LIFETIME
        else:
            return True

    def is_entry_valid(self, entry: dict) -> bool:
        return self.entry_has_keys(entry, ['link', 'title'])

    def keep_entry(self, entry: FeedParserDict) -> bool:
        return True

    def keep_item(self, item: Item) -> bool:
        return True

    def parse_entries(self, entries: list[FeedParserDict], now: datetime) -> list[Item]:
        items = []
        for entry in entries:
            if (
                    self.is_entry_valid(entry)
                    and self.is_entry_recent(entry, now)
                    and self.keep_entry(entry)
            ):
                item = self.parse_entry(entry, now)
                if self.keep_item(item):
                    items.append(item)
        return items

    def parse_entry(self, entry: FeedParserDict, now: datetime) -> Item:
        url = URL(entry.link)
        return Item(
            url=url,
            title=entry.title,
            sources=[Source(url, self.initials)],
            created=now,
            modified=now,
        )

    def update_from(self, other: 'Feed'):
        if other.etag:
            self.etag = other.etag
        if other.last_modified:
            self.last_modified = other.last_modified

    @staticmethod
    def decode(encoded: JSONDict, options: dict) -> 'Feed':
        return Feed(
            options=options,
            name=encoded['name'],
            initials=encoded['initials'],
            feed_url=URL(encoded['feed_url']),
            etag=encoded.get('etag'),
            last_modified=encoded.get('last_modified'),
        )

    def encode(self) -> JSONDict:
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
