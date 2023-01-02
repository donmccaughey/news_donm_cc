import json

from datetime import datetime, timedelta, timezone
from typing import Iterable, Any

from .item import Item
from .utility import bisect


class News:
    def __init__(self,
                 items: list[Item] = [],
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 lifetime: timedelta | None = timedelta(days=30),
                 ):
        self.items = list(items)
        self.index = set(items)

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now
        self.lifetime = lifetime
        self.expired = self.modified - self.lifetime
        self.is_modified = False

    def __iter__(self) -> Iterable[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        modified = ', modified' if self.is_modified else ''
        return f'<News: {len(self.items)} items{modified}>'

    def __str__(self) -> str:
        modified = ' (modified)' if self.is_modified else ''
        return f'{len(self.items)} news items{modified}'

    def add_new(self, other: 'News') -> int:
        new_count = 0
        for item in other:
            if item not in self.index:
                self.items.insert(0, item)
                self.index.add(item)
                self.modified = other.modified
                self.is_modified = True
                self.expired = self.modified - self.lifetime
                new_count += 1
        return new_count

    def remove_old(self) -> int:
        i = bisect(self.items, lambda item: item.created > self.expired)
        if i == len(self.items):
            return 0

        self.is_modified = True
        old_items = self.items[i:]
        self.index.difference_update(old_items)
        del self.items[i:]
        return len(old_items)

    @staticmethod
    def decode(encoded: dict[str, Any]) -> 'News':
        items = encoded['items']
        return News(
            items=[Item.decode(item) for item in items],
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> dict[str, Any]:
        return {
            'items': [item.encode() for item in self.items],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
            'expired': datetime.isoformat(self.expired),
        }

    @staticmethod
    def from_json(s: str) -> 'News':
        return News.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
