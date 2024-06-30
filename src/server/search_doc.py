from collections.abc import Iterator

from news import Item
from .cached_news import CachedNews
from .doc import Doc
from .utility import count_phrase


class SearchDoc(Doc[Item]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            query: str,
    ):
        super().__init__(cached_news, version, is_styled)
        self.query = query
        self.items = self.news.search(query)
        self.count_phrase = count_phrase(self.items, 'item')

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
