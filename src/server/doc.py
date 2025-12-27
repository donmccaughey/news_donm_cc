from collections.abc import Iterable, Iterator, Sized
from jinja2 import Template
from typing import TypeVar, Union

from jsontype import JSONDict, JSONList
from news import News


T = TypeVar('T')

Representation = Union[
    JSONDict,
    JSONList,
    Template,
    str,
    list[str | Template],
]


class Doc(Iterable[T], Sized):
    def __init__(self, news: News, version: str, is_styled: bool):
        self.is_styled = is_styled
        self.news = news
        self.version = version

        self.modified = self.news.modified

        self.counter_reset_item = 0
        self.first_item_index = 0

    def __iter__(self) -> Iterator[T]:
        raise NotImplementedError()

    def __len__(self) -> int:
        raise NotImplementedError()

    def get_representation(self) -> Representation:
        raise NotImplementedError()
