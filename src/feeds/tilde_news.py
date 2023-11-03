from news.url import URL
from .aggregator import Aggregator


class TildeNews(Aggregator):
    def __init__(self):
        super().__init__('tilde.news', '~n', URL('https://tilde.news/rss'))

    def __repr__(self) -> str:
        return 'TildeNews()'
