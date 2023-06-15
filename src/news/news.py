import json

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Iterable

from utility.jsontype import JSONDict
from .item import Age, Item


LIFETIME = timedelta(days=30)


class News:

    def __init__(self,
                 items: list[Item] = None,
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 lifetime: timedelta | None = LIFETIME,
                 ):
        self.ordered_items = list()
        self.unique_items = dict()
        self.by_site = defaultdict(list)

        now = datetime.now(timezone.utc)
        self.created = created or now
        self.modified = modified or now
        self.lifetime = lifetime
        self.is_modified = False

        for item in (items or []):
            self.add_item(item, at_head=False)

    def __iter__(self) -> Iterable[Item]:
        return iter(self.ordered_items)

    def __len__(self) -> int:
        return len(self.ordered_items)

    def __repr__(self) -> str:
        modified = ', modified' if self.is_modified else ''
        return f'<News: {len(self.ordered_items)} items{modified}>'

    def __str__(self) -> str:
        modified = ' (modified)' if self.is_modified else ''
        return f'{len(self.ordered_items)} news items{modified}'

    @property
    def items(self) -> list[Item]:
        return self.ordered_items

    def add_item(self, item: Item, *, at_head: bool):
        item.age = Age.NEW if self.modified == item.modified else Age.OLD
        self.unique_items[item] = item
        if at_head:
            self.ordered_items.insert(0, item)
        else:
            self.ordered_items.append(item)
        self.by_site[item.url.identity].append(item)

    @property
    def expired(self) -> datetime:
        return self.modified - self.lifetime

    def remove_item_at(self, i: int):
        item = self.ordered_items[i]
        identity = item.url.identity

        del self.unique_items[item]

        self.by_site[identity].remove(item)
        if not self.by_site[identity]:
            del self.by_site[identity]

        del self.ordered_items[i]

    def remove_old(self, now: datetime) -> int:
        old_count = 0
        i = len(self.ordered_items) - 1
        while i >= 0 and self.ordered_items[i].created <= self.expired:
            self.remove_item_at(i)
            self.modified = now
            self.is_modified = True
            old_count += 1
            i -= 1
        if self.is_modified:
            self.update_ages()
        return old_count

    def update(self, other: 'News') -> tuple[int, int]:
        new_count, modified_count = 0, 0
        new_items = [item for item in other if item not in self.unique_items]
        if new_items:
            self.modified = other.modified
            self.is_modified = True
            self.update_ages()
            for item in reversed(new_items):
                self.add_item(item, at_head=True)
                new_count += 1
        return new_count, modified_count

    def update_ages(self):
        i = 0
        while i < len(self.ordered_items) and self.ordered_items[i].age == Age.NEW:
            self.ordered_items[i].age = (
                Age.NEW if self.modified == self.ordered_items[i].modified else Age.OLD
            )
            i += 1

    @staticmethod
    def decode(encoded: JSONDict) -> 'News':
        items = [Item.decode(item) for item in encoded['items']]
        for item in items:
            for source in item.sources:
                if source.site_id == 'tn':
                    source.site_id = '~n'
        return News(
            items=items,
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> JSONDict:
        return {
            'items': [item.encode() for item in self.ordered_items],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
            'expired': datetime.isoformat(self.expired),
        }

    @staticmethod
    def from_json(s: str) -> 'News':
        return News.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
