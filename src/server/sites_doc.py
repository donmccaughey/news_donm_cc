from dataclasses import dataclass
from typing import Iterable, Iterator

from news import Item
from .cached_news import CachedNews
from .utility import count_phrase


@dataclass
class Site:
    count_phrase: str
    identity: str
    items: list[Item]


class SitesDoc(Iterable[Site]):
    def __init__(
            self,
            cached_news: CachedNews,
            version: str,
            is_styled: bool,
    ):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.sites = [
            Site(
                count_phrase(self.news.by_site[site], 'item'),
                site,
                self.news.by_site[site]
            )
            for site in sorted(self.news.by_site.keys())
        ]
        self.modified = self.news.modified

        self.counter_reset_item = 0
        self.count_phrase = count_phrase(self.sites, 'site')
        self.first_item_index = 0

    def __iter__(self) -> Iterator[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)
