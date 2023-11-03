from news import Item
from news.url import URL
from .aggregator import Aggregator
from .skip_sites import SKIP_SITES


class HackerNews(Aggregator):
    def __init__(self):
        super().__init__(
            'Hacker News',
            'hn',
            URL('https://news.ycombinator.com/rss'),
        )

    def __repr__(self) -> str:
        return 'HackerNews()'

    def keep_item(self, item: Item) -> bool:
        return item.url.identity not in SKIP_SITES
