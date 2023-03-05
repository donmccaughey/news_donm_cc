from typing import Iterable

from news import News, Item
from utility import Cache

from .utility import count_phrase


class SitePage:
    def __init__(self, news_cache: Cache, version: str, identity: str):
        self.version = version
        self.identity = identity

        self.news = News.from_json(news_cache.get() or News().to_json())
        self.items = self.news.by_site[self.identity]
        self.modified = self.news.modified

        self.counter_reset_item = 0
        self.count_phrase = count_phrase(self.items, 'item')

    def __iter__(self) -> Iterable[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
