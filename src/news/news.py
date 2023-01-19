import json

from datetime import datetime, timedelta, timezone
from typing import Iterable, Any

from .item import Age, Item


LIFETIME = timedelta(days=30)


class News:

    def __init__(self,
                 items: list[Item] = [],
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 lifetime: timedelta | None = LIFETIME,
                 ):
        self.items = list()
        self.index = set()

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now
        self.lifetime = lifetime
        self.is_modified = False

        for item in items:
            self.add_item(item, at_head=False)

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

    def add_item(self, item: Item, *, at_head: bool):
        item.age = Age.NEW if self.modified == item.modified else Age.OLD
        self.index.add(item)
        if at_head:
            self.items.insert(0, item)
        else:
            self.items.append(item)

    def add_new(self, other: 'News') -> int:
        new_items = [item for item in other if item not in self.index]
        if new_items:
            self.modified = other.modified
            self.is_modified = True
            self.update_ages()
            for item in reversed(new_items):
                self.add_item(item, at_head=True)
        return len(new_items)

    @property
    def expired(self) -> datetime:
        return self.modified - self.lifetime

    def remove_old(self, now: datetime) -> int:
        old_count = 0
        i = len(self.items) - 1
        while i >= 0 and self.items[i].created <= self.expired:
            self.index.remove(self.items[i])
            del self.items[i]
            self.modified = now
            self.is_modified = True
            old_count += 1
            i -= 1
        if self.is_modified:
            self.update_ages()
        return old_count

    def update_ages(self):
        i = 0
        while i < len(self.items) and self.items[i].age == Age.NEW:
            self.items[i].age = (
                Age.NEW if self.modified == self.items[i].modified else Age.OLD
            )
            i += 1

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
