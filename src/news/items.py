import json
from datetime import datetime, timezone
from typing import Iterable

from .item import Item


class Items:
    def __init__(self,
                 items: list[Item] | None = None,
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 ):
        self.items = items if items else list()
        self.index = {item.source: item for item in items} if items else dict()

        now = datetime.now(timezone.utc)
        self.created = created if created else now
        self.modified = modified if modified else now

    def __iadd__(self, other: 'Items'):
        for item in other:
            if item.source in self.index:
                # TODO: update item
                pass
            else:
                self.items.append(item)
                self.index[item.source] = item
                self.modified = other.modified
        return self

    def __iter__(self) -> Iterable:
        return iter(self.items)

    def __repr__(self) -> str:
        return f'Items<count = {len(self.items)}>'

    def __str__(self) -> str:
        return f'{len(self.items)} items updated on {self.modified}'

    def prune(self, cutoff: datetime):
        self.items = [item for item in self.items if item.created > cutoff]

    @staticmethod
    def decode(encoded: dict) -> 'Items':
        return Items(
            items=[Item.decode(item) for item in encoded['stories']],
            created=datetime.fromisoformat(encoded['created']),
            modified=datetime.fromisoformat(encoded['modified']),
        )

    def encode(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            'stories': [item.encode() for item in self.items],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }

    @staticmethod
    def from_json(s: str) -> 'Items':
        return Items.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
