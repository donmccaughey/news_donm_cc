from typing import Iterable, Iterator, Optional

from news import Item
from serialize import JSONList


class Page(Iterable[Item]):
    def __init__(self, items: list[Item], page_number: int, items_per_page: int):
        self.items = items
        self.number = page_number
        self.items_per_page = items_per_page

        self.index = self.number - 1
        self.begin = self.index * self.items_per_page
        self.end = self.begin + self.items_per_page

        items_end = len(self.items)
        if items_end < self.end:
            self.end = items_end
        if self.begin > self.end:
            self.begin = self.end

        self.count = ((items_end - 1) // self.items_per_page) + 1

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items[self.begin:self.end])

    def __len__(self) -> int:
        return self.end - self.begin

    def __repr__(self) -> str:
        return f'<Page {self.number} of {self.count}, items[{self.begin}:{self.end}]>'

    def __str__(self) -> str:
        return f'Page {self.number} of {self.count}'

    @property
    def is_valid(self) -> bool:
        return (
                (1 <= self.number <= self.count)
                or (self.number == 1 and self.count == 0)
        )

    @property
    def first(self) -> Optional['Page']:
        if self.number != 1 and self.count > 1:
            return Page(self.items, 1, self.items_per_page)
        else:
            return None

    @property
    def last(self) -> Optional['Page']:
        if self.number != self.count and self.count > 1:
            return Page(self.items, self.count, self.items_per_page)
        else:
            return None

    @property
    def next(self) -> Optional['Page']:
        if self.number < self.count:
            return Page(self.items, self.number + 1, self.items_per_page)
        else:
            return None

    @property
    def previous(self) -> Optional['Page']:
        if self.number > 1:
            return Page(self.items, self.number - 1, self.items_per_page)
        else:
            return None

    def to_json(self) -> JSONList:
        return [item.encode() for item in self]
