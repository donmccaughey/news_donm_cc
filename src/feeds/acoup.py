from news import URL
from .feed import Feed


class Acoup(Feed):
    def __init__(self):
        super().__init__(
            'A Collection of Unmitigated Pedantry',
            'acoup',
            URL('https://acoup.blog/feed/')
        )

    def __repr__(self) -> str:
        return 'Acoup()'
