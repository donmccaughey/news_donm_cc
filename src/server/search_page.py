from typing import Iterable, Iterator

from news import Item
from .cached_news import CachedNews
from .utility import count_phrase


class SearchPage(Iterable[Item]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            query: str,
    ):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.modified = self.news.modified

        self.query = query
        self.items = self.news.search(query)

        self.counter_reset_item = 0
        self.count_phrase = count_phrase(self.items, 'item')
        self.first_item_value = 1

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
