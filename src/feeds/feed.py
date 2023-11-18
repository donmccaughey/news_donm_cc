import calendar
import logging
from datetime import datetime, timezone
from typing import cast
from io import BytesIO

import requests
from feedparser import FeedParserDict, parse

from news import LIFETIME, Item, Source
from news.url import NormalizedURL, URL
from serialize import Encodable, JSONDict, JSONList


log = logging.getLogger(__name__)


class Feed(Encodable):
    def __init__(self,
                 name: str,
                 initials: str,
                 url: URL | None = None,
                 etag: str | None = None,
                 last_modified: str | None = None,
                 ):
        self.name = name
        self.initials = initials
        self.url = url
        self.etag = etag
        self.last_modified = last_modified

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Feed) and self.name == other.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __repr__(self) -> str:
        return f"Feed('{self.name}', '{self.initials}', {repr(self.url)})"

    def __str__(self) -> str:
        return str(self.name)

    def entry_has_keys(self, entry: dict, keys: list[str]) -> bool:
        for key in keys:
            if key not in entry:
                log.warning(f'Entry {repr(entry)} from {self.name} does not have a "{key}" attribute')
                return False
        return True

    def get_items(self, now: datetime) -> list[Item]:
        assert self.url

        try:
            headers = {'User-Agent': 'News +https://news.donm.cc'}
            if self.etag:
                headers['If-None-Match'] = self.etag
            if self.last_modified:
                headers['If-Modified-Since'] = self.last_modified
            response = requests.get(str(self.url), headers=headers, timeout=2)
        except Exception as e:
            log.warning(f'{self.name} failed: {repr(e)}')
            return []

        if response.status_code in [200, 302]:  # OK, Found
            if 'etag' in response.headers:
                self.etag = response.headers['ETag']
            if 'modified' in response.headers:
                self.last_modified = response.headers['Last-Modified']
            content = BytesIO(response.content)
            d: FeedParserDict = parse(content)
            return self.parse_entries(d.entries, now)
        elif response.status_code in [301, 308]:  # Moved Permanently, Permanent Redirect
            log.warning(f'{self.name} returned status code {response.status_code}: {response.headers["Location"]}')
            return []
        elif response.status_code == 304:  # Not Modified
            return []
        else:
            log.warning(f'{self.name} returned status code {response.status_code}')
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
            if published > now:
                skew = published - now
                log.warning(
                    f'{self.name} entry "{entry.get("title")}" '
                    f'has a published date in the future: '
                    f'now = {now}, '
                    f'published = {published}, '
                    f'skew = {skew}'
                )
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
        url = NormalizedURL(entry.link)
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
    def decode(encoded: JSONDict | JSONList) -> 'Feed':
        encoded = cast(JSONDict, encoded)
        return Feed(
            name=cast(str, encoded['name']),
            initials=cast(str, encoded['initials']),
            etag=cast(str | None, encoded.get('etag')),
            last_modified=cast(str | None, encoded.get('last_modified')),
        )

    def encode(self) -> JSONDict:
        encoded: JSONDict = {
            'name': self.name,
            'initials': self.initials,
        }
        if self.etag:
            encoded['etag'] = self.etag
        if self.last_modified:
            encoded['last_modified'] = self.last_modified
        return encoded
