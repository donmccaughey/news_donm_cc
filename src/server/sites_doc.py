from collections.abc import Iterator
from dataclasses import dataclass

from flask import render_template

from news import Item
from .cached_news import CachedNews
from .doc import Doc
from .doc import Representation
from .utility import count_phrase


@dataclass
class Site:
    count_phrase: str
    identity: str
    items: list[Item]


class SitesDoc(Doc[Site]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
    ):
        super().__init__(cached_news, version, is_styled)
        self.sites = [
            Site(
                count_phrase(self.news.items_by_site[site], 'item'),
                site,
                self.news.items_by_site[site]
            )
            for site in sorted(self.news.items_by_site.keys())
        ]
        self.count_phrase = count_phrase(self.sites, 'site')

    def __iter__(self) -> Iterator[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)

    def get_representation(self) -> Representation:
        return render_template('sites.html', doc=self)
