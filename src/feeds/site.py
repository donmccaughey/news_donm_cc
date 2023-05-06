import calendar
import logging
import time
from datetime import datetime, timezone
from typing import Any

from feedparser import FeedParserDict, parse

from news import LIFETIME, Item, News, URL

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
        if 'status' not in d:
            log.warning(f'{self.name} failed without status code')
            return News()
        if d.status in [200, 302]:
            if 'etag' in d:
                self.etag = d.etag
            if 'modified' in d:
                self.last_modified = d.modified
            if self.etag or self.last_modified:
                log.debug(f'{self.name}: etag={self.etag}, last_modified={self.last_modified}')
            return News(
                items=self.parse_entries(d.entries, now),
                created=now,
                modified=now,
            )
        elif d.status == 304:
            log.debug(f'{self.name} is unmodified')
            return News()
        else:
            log.warning(f'{self.name} returned status code {d.status}')
            return News()

    def parse_entries(self, entries: list[FeedParserDict], now: datetime) -> list[Item]:
        items = []
        for entry in entries:
            if not is_recent(entry, now):
                continue
            if not self.keep_entry(entry):
                continue
            items.append(self.parse_entry(entry, now))
        return items

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


def is_recent(entry, now: datetime) -> bool:
    time_tuple = (
        entry.published_parsed
        or entry.updated_parsed
        or entry.created_parsed
        or time.gmtime()
    )
    timestamp = calendar.timegm(time_tuple)
    published = datetime.fromtimestamp(timestamp, timezone.utc)
    return now - published < LIFETIME
