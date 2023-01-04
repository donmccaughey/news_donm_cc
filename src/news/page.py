from typing import Iterable, Optional


class Page:
    def __init__(self, items: list, page_number: int, items_per_page: int):
        self.items = items
        self.items_per_page = items_per_page
        self.number = page_number

        self.begin = (self.number - 1) * self.items_per_page
        self.end = self.begin + self.items_per_page

        items_end = len(self.items)
        if items_end < self.end:
            self.end = items_end
        if self.begin > self.end:
            self.begin = self.end

        self.count = ((items_end - 1) // self.items_per_page) + 1

    def __iter__(self) -> Iterable:
        return iter(self.items[self.begin:self.end])

    def __len__(self) -> int:
        return self.end - self.begin

    def __repr__(self) -> str:
        return f'<Page {self.number} of {self.count}, items[{self.begin}:{self.end}]>'

    def __str__(self) -> str:
        return f'Page {self.number} of {self.count}'

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

    @classmethod
    def one_page(cls, items: list) -> 'Page':
        return Page(items, 1, len(items))
