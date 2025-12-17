from collections.abc import Iterator

from flask import render_template

from news import Item, News
from .doc import Doc, Representation
from .utility import count_phrase


class SearchDoc(Doc[Item]):
    def __init__(self, news: News, version: str, is_styled: bool, query: str):
        super().__init__(news, version, is_styled)
        self.query = query
        self.items = self.news.search(query)
        self.count_phrase = count_phrase(self.items, 'item')

    def __iter__(self) -> Iterator[Item]:
        return iter(self.items)

    def __len__(self) -> int:
        return len(self.items)

    def get_representation(self) -> Representation:
        return render_template('search.html', doc=self)
