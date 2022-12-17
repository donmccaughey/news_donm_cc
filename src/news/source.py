from datetime import datetime

from .item import Item
from .items import Items
from .url import URL


class Source:
    def __init__(self, url: URL):
        self.url = url

    def __repr__(self) -> str:
        return f'Source<{self.url}>'

    def __str__(self) -> str:
        return self.url

    def get(self, now: datetime) -> Items:
        items = [
            Item(
                url=URL('https://example.com/story1'),
                title='Story 1',
                source=URL('https://source.com/story1'),
            )
        ]
        return Items(items=items)
