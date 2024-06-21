from typing import Iterable, Iterator

from flask import url_for

from news import Item
from serialize import JSONDict
from utility import Page
from .cached_news import CachedNews


class NewsPage(Iterable[Item]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            page_number: int,
            full_urls: bool,
    ):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.modified = self.news.modified

        self.page = Page(
            self.news.items, page_number=page_number, items_per_page=10
        )
        self.is_valid = (
            (1 <= self.page.number <= self.page.count)
            or (self.page.number == 1 and self.page.count == 0)
        )

        self.counter_reset_item = self.page.begin
        self.first_item_value = self.page.begin + 1

        # navigation URLs
        self.first_url = page_url(self.page.first, full_urls)
        self.last_url = page_url(self.page.last, full_urls)
        self.next_url = page_url(self.page.next, full_urls)
        self.previous_url = page_url(self.page.previous, full_urls)

    def __iter__(self) -> Iterator[Item]:
        return iter(self.page)

    def to_json(self) -> JSONDict:
        json = {
            'version': self.version,
            'modified': self.modified.isoformat(),
            'page_number': self.page.number,
            'items': self.page.to_json(),
            'first_url': self.first_url,
            'last_url': self.last_url,
            'next_url': self.next_url,
            'previous_url': self.previous_url,
        }

        return json


def page_url(page: Page, full_url: bool) -> str | None:
    if not page:
        return None
    if page.number == 1:
        return url_for('first_page', _external=full_url)
    return url_for(
        'numbered_page', page_number=page.number, _external=full_url
    )
