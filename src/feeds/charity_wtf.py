from news import URL
from .feed import Feed


class CharityWTF(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            URL('https://charity.wtf/feed/'),
            'charity.wtf',
            'cw',
        )

    def __repr__(self) -> str:
        return 'CharityWTF()'
