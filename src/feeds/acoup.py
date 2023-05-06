from news import URL
from .site import Site


class Acoup(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://acoup.blog/feed/'),
            'A Collection of Unmitigated Pedantry', 'acoup',
        )

    def __repr__(self) -> str:
        return 'Acoup()'
