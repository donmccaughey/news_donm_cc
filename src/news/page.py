from typing import Iterable, Optional

from .news import News


class Page:
    def __init__(self, news: News, page_number: int, items_per_page: int):
        self.news = news
        self.items_per_page = items_per_page
        self.number = page_number

        self.begin = (self.number - 1) * self.items_per_page
        self.end = self.begin + self.items_per_page
        items_end = len(self.news)
        if items_end < self.end:
            self.end = items_end

        self.count = ((items_end - 1) // self.items_per_page) + 1

    def __iter__(self) -> Iterable:
        return iter(self.news.items[self.begin:self.end])

    def __len__(self) -> int:
        return self.end - self.begin

    def __repr__(self) -> str:
        return f'Page<size={self.items_per_page}, start={self.number}>'

    def __str__(self) -> str:
        return f'Page {self.number} of {self.count}'

    @property
    def last(self) -> Optional['Page']:
        if self.number != self.count and self.count > 1:
            return Page(self.news, self.count, self.items_per_page)
        else:
            return None

    @property
    def next(self) -> Optional['Page']:
        if self.number < self.count:
            return Page(self.news, self.number + 1, self.items_per_page)
        else:
            return None

    @property
    def previous(self) -> Optional['Page']:
        if self.number > 1:
            return Page(self.news, self.number - 1, self.items_per_page)
        else:
            return None

    @classmethod
    def one_page(cls, news: News) -> 'Page':
        return Page(news, 1, len(news))
