from news.url import URL
from .aggregator import Aggregator


class Lobsters(Aggregator):
    def __init__(self):
        super().__init__('Lobsters', 'lob', URL('https://lobste.rs/rss'))

    def __repr__(self) -> str:
        return 'Lobsters()'
