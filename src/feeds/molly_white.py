from news.url import URL
from .feed import Feed


class MollyWhite(Feed):
    def __init__(self):
        super().__init__(
            'Molly White',
            'mw',
            URL('https://newsletter.mollywhite.net/feed')
        )

    def __repr__(self) -> str:
        return 'MollyWhite()'
