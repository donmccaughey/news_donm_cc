from news import URL
from .feed import Feed


class CharityWTF(Feed):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://charity.wtf/feed/'),
            'charity.wtf', 'cw',
        )

    def __repr__(self) -> str:
        return 'CharityWTF()'
