from collections.abc import Iterable, Iterator, Sized
from typing import TypeVar
from .cached_news import CachedNews


T = TypeVar('T')


class Doc(Iterable[T], Sized):
    def __init__(self, cached_news: CachedNews, version: str, is_styled: bool):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.modified = self.news.modified

        self.counter_reset_item = 0
        self.first_item_index = 0

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()
