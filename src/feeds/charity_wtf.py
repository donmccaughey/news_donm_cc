from news import URL
from .site import Site


class CharityWTF(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://charity.wtf/feed/'),
            'charity.wtf', 'cw',
        )

    def __repr__(self) -> str:
        return 'CharityWTF()'
