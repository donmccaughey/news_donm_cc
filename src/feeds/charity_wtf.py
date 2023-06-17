from news import URL
from .feed import Feed


class CharityWTF(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'charity.wtf',
            'cw',
            URL('https://charity.wtf/feed/')
        )

    def __repr__(self) -> str:
        return 'CharityWTF()'
