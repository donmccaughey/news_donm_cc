from collections.abc import Iterator

from news import Item
from .cached_news import CachedNews
from .doc import Doc
from .utility import count_phrase


class SiteDoc(Doc[Item]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            identity: str,
    ):
        super().__init__(cached_news, version, is_styled)
        self.identity = identity
        self.items = self.news.by_site[self.identity]
        self.count_phrase = count_phrase(self.items, 'item')

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)
