import json

from collections import defaultdict
from collections.abc import Container
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sized
from datetime import datetime, timedelta, timezone
from typing import cast

from serialize import Encodable, JSONDict, JSONList, Serializable
from .index import Index
from .item import Item


LIFETIME = timedelta(days=15)


class News(Container[Item], Encodable, Iterable[Item], Serializable, Sized):
    def __init__(self,
                 items: list[Item] | None = None,
                 created: datetime | None = None,
                 modified: datetime | None = None,
                 lifetime: timedelta | None = LIFETIME,
                 ):
        self.__index: Index | None = None

        self.__ordered_items: list[Item] = list()
        self.__unique_items: dict[Item, Item] = dict()
        self.__by_site: dict[str, list[Item]] = defaultdict(list)

        now = datetime.now(timezone.utc)
        self.created = created or now
        self.modified = modified or now
        self.lifetime = lifetime or LIFETIME

        for item in reversed(items or []):
            self.add_item(item)

    def __contains__(self, item) -> bool:
        return item in self.__unique_items

    def __iter__(self) -> Iterator[Item]:
        return iter(self.__ordered_items)

    def __len__(self) -> int:
        return len(self.__ordered_items)

    def __repr__(self) -> str:
        return f'<News: {len(self)} items>'

    def __str__(self) -> str:
        return f'{len(self)} news items'

    @property
    def index(self) -> Index:
        if not self.__index:
            self.__index = Index.from_items(self)
        return self.__index

    @property
    def items(self) -> list[Item]:
        return self.__ordered_items

    @property
    def items_by_site(self) -> dict[str, list[Item]]:
        return self.__by_site

    def add_item(self, item: Item):
        if not item.seq_id:
            last_seq_id = self.__ordered_items[0].seq_id if self.__ordered_items else 0
            item.seq_id = last_seq_id + 1
        self.__ordered_items.insert(0, item)
        self.__unique_items[item] = item
        self.__by_site[item.url.identity].insert(0, item)

    def remove_item_at(self, i: int):
        item = self.__ordered_items[i]
        del self.__ordered_items[i]

        if item in self.__unique_items:
            del self.__unique_items[item]

        identity = item.url.identity
        if identity in self.__by_site:
            if item in self.__by_site[identity]:
                self.__by_site[identity].remove(item)
            if not self.__by_site[identity]:
                del self.__by_site[identity]

    def remove_old(self, now: datetime) -> int:
        expiration_date = now - self.lifetime
        old_count = 0
        i = len(self) - 1
        while i >= 0 and self.items[i].created <= expiration_date:
            self.remove_item_at(i)
            self.modified = now
            old_count += 1
            i -= 1
        return old_count

    def search(self, query: str) -> list[Item]:
        indices = sorted(self.index.search(query))
        return [self.items[i] for i in indices]

    def update(self, items: list[Item], now: datetime) -> tuple[int, int]:
        new_items, existing_items = [], []
        for item in items:
            if item in self:
                existing_items.append(item)
            else:
                new_items.append(item)
        if new_items or existing_items:
            self.modified = now
        for new_item in reversed(new_items):
            self.add_item(new_item)
        for existing_item in existing_items:
            self.__unique_items[existing_item].update_from(existing_item)
        return len(new_items), len(existing_items)

    @staticmethod
    def decode(encoded: JSONDict | JSONList) -> 'News':
        encoded = cast(JSONDict, encoded)
        items = [
            Item.decode(cast(JSONDict, item))
            for item in cast(JSONList, encoded['items'])
        ]
        return News(
            items=items,
            created=datetime.fromisoformat(cast(str, encoded['created'])),
            modified=datetime.fromisoformat(cast(str, encoded['modified'])),
        )

    def encode(self) -> JSONDict:
        return {
            'items': [item.encode() for item in self],
            'created': datetime.isoformat(self.created),
            'modified': datetime.isoformat(self.modified),
        }

    @staticmethod
    def from_json(s: str) -> 'News':
        return News.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
