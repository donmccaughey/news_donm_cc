from dataclasses import dataclass
from typing import Iterable, Iterator

from news import Item, News
from server.utility import count_phrase
from utility import CachedFile


@dataclass
class Site:
    count_phrase: str
    identity: str
    items: list[Item]


class SitesPage(Iterable[Site]):
    def __init__(
            self,
            news_cache: CachedFile,
            version: str,
            is_styled: bool,
    ):
        self.is_styled = is_styled
        self.version = version

        self.news = News.from_json(news_cache.read() or News().to_json())
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
        self.first_item_value = 1

    def __iter__(self) -> Iterator[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)
