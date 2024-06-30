from collections.abc import Iterator
from dataclasses import dataclass

from news import Item
from .cached_news import CachedNews
from .doc import Doc
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
                count_phrase(self.news.by_site[site], 'item'),
                site,
                self.news.by_site[site]
            )
            for site in sorted(self.news.by_site.keys())
        ]
        self.count_phrase = count_phrase(self.sites, 'site')

    def __iter__(self) -> Iterator[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)
