from collections.abc import Iterator

from flask import render_template
from flask import url_for
from werkzeug.datastructures import MIMEAccept

from news import Item
from serialize import JSONDict
from utility import Page
from .cached_news import CachedNews
from .doc import Doc, Representation


class NewsDoc(Doc[Item]):
    ACCEPTED = ['application/json', 'text/html']

    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
            accept_mimetypes: MIMEAccept,
            page_number: int,
    ):
        super().__init__(cached_news, version, is_styled)

        self.accepts_json = (
                'application/json' == accept_mimetypes.best_match(self.ACCEPTED)
        )
        if self.accepts_json:
            items_per_page = 100
            full_urls = True
        else:
            items_per_page = 10
            full_urls = False

        self.page = Page(self.news.items, page_number, items_per_page)
        self.counter_reset_item = self.page.begin
        self.first_item_index = self.page.begin

        self.first_url = page_url(self.page.first, full_urls)
        self.last_url = page_url(self.page.last, full_urls)
        self.next_url = page_url(self.page.next, full_urls)
        self.previous_url = page_url(self.page.previous, full_urls)

    def __iter__(self) -> Iterator[Item]:
        return iter(self.page)

    def __len__(self) -> int:
        return self.page.count

    def get_representation(self) -> Representation:
        return (
            self.to_json() if self.accepts_json
            else render_template('news.html', doc=self)
        )

    def to_json(self) -> JSONDict:
        return {
            'version': self.version,
            'modified': self.modified.isoformat(),
            'page_index': self.page.index,
            'total_pages': self.page.count,
            'items_per_page': self.page.items_per_page,
            'items': self.page.to_json(),
            'first_item_index': self.first_item_index,
            'total_items:': len(self.news.items),
            'first_url': self.first_url,
            'last_url': self.last_url,
            'next_url': self.next_url,
            'previous_url': self.previous_url,
        }


def page_url(page: Page | None, full_url: bool) -> str | None:
    if not page:
        return None
    if page.number == 1:
        return url_for('home', _external=full_url)
    return url_for(
        'numbered', page_number=page.number, _external=full_url
    )
