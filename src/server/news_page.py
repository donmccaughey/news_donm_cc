from typing import Iterable

from news import News, Item
from utility import Cache, Page


class NewsPage:
    def __init__(self, news_cache: Cache, version: str, page_number: int):
        self.version = version

        self.news = News.from_json(news_cache.get() or News().to_json())
        self.modified = self.news.modified

        self.page = Page(self.news.items, page_number=page_number, items_per_page=10)
        self.is_valid = (
            (1 <= self.page.number <= self.page.count)
            or (self.page.number == 1 and self.page.count == 0)
        )

        self.counter_reset_item = self.page.begin

        # navigation URLs
        self.first_url = './' if self.page.number > 1 else None

        last_page = self.page.last
        self.last_url = f'./{last_page.number}' if last_page else None

        next_page = self.page.next
        self.next_url = f'./{next_page.number}' if next_page else None

        previous_page = self.page.previous
        if previous_page:
            self.previous_url = './' if previous_page.number == 1 else f'./{previous_page.number}'
        else:
            self.previous_url = None

    def __iter__(self) -> Iterable[Item]:
        return iter(self.page)
