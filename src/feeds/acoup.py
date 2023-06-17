from news import URL
from .feed import Feed


class Acoup(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            URL('https://acoup.blog/feed/'),
            'A Collection of Unmitigated Pedantry',
            'acoup',
        )

    def __repr__(self) -> str:
        return 'Acoup()'
