import json
from datetime import datetime, timezone
from typing import Iterable

from .item import Item


class News:
    def __init__(self,
                 items: list[Item] = [],
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 ):
        self.items = list(items)
        self.index = set(items)

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now
        self.is_modified = False

    def __iter__(self) -> Iterable:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def __repr__(self) -> str:
        modified = ', modified' if self.is_modified else ''
        return f'<News: {len(self.items)} items{modified}>'

    def __str__(self) -> str:
        modified = ' (modified)' if self.is_modified else ''
        return f'{len(self.items)} news items{modified}'

    def add_new(self, other: 'News'):
        for item in other:
            if item not in self.index:
                self.items.insert(0, item)
                self.index.add(item)
                self.modified = other.modified
                self.is_modified = True
        return self

    def remove_old(self, cutoff: datetime):
        items = []
        for item in self.items:
            if item.created > cutoff:
                items.append(item)
            else:
                self.is_modified = True
                self.index.remove(item)
        self.items = items

    @staticmethod
    def decode(encoded: dict) -> 'News':
        items = encoded['items'] if 'items' in encoded else encoded['stories']
        return News(
            items=[Item.decode(item) for item in items],
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            'items': [item.encode() for item in self.items],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }

    @staticmethod
    def from_json(s: str) -> 'News':
        return News.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
