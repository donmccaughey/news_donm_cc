from typing import Iterable, Iterator

from news import Item
from utility import Page
from .cached_news import CachedNews


class NewsPage(Iterable[Item]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            page_number: int,
    ):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.modified = self.news.modified

        self.page = Page(self.news.items, page_number=page_number, items_per_page=10)
        self.is_valid = (
            (1 <= self.page.number <= self.page.count)
            or (self.page.number == 1 and self.page.count == 0)
        )

        self.counter_reset_item = self.page.begin
        self.first_item_value = self.page.begin + 1

        # navigation URLs
        self.first_url = './' if self.page.number > 1 else None

        last_page = self.page.last
        self.last_url = f'./{last_page.number}' if last_page else None

        next_page = self.page.next
        self.next_url = f'./{next_page.number}' if next_page else None

        self.previous_url: str | None = None
        previous_page = self.page.previous
        if previous_page:
            self.previous_url = './' if previous_page.number == 1 else f'./{previous_page.number}'

    def __iter__(self) -> Iterator[Item]:
        return iter(self.page)
