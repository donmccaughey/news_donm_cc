from collections import defaultdict
from collections.abc import Container
from collections.abc import Iterable
from collections.abc import Iterator
from collections.abc import Sized

from .item import Item


class Items(Container[Item], Iterable[Item], Sized):
    def __init__(self, items: list[Item] | None = None):
        self.__ordered_items: list[Item] = list()
        self.__unique_items: dict[Item, Item] = dict()
        self.__by_site: dict[str, list[Item]] = defaultdict(list)
        for item in reversed(items or []):
            self.add_item(item)

    def __contains__(self, item) -> bool:
        return item in self.__unique_items

    def __iter__(self) -> Iterator[Item]:
        return iter(self.__ordered_items)

    def __len__(self) -> int:
        return len(self.__ordered_items)

    def __repr__(self) -> str:
        return f'<Items: {len(self)} items>'

    def __str__(self) -> str:
        return f'{len(self)} items'

    @property
    def items(self) -> list[Item]:
        return self.__ordered_items

    @property
    def by_site(self) -> dict[str, list[Item]]:
        return self.__by_site

    def add_item(self, item: Item):
        if not item.seq_id:
            last_seq_id = (
                self.__ordered_items[0].seq_id if self.__ordered_items else 0
            )
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

    def update_item(self, item: Item):
        self.__unique_items[item].update_from(item)
