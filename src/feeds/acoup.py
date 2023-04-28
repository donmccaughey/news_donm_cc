from datetime import datetime

from news import Item, Source, URL
from .site import Site


class Acoup(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://acoup.blog/feed/'),
            'A Collection of Unmitigated Pedantry', 'acoup',
        )

    def __repr__(self) -> str:
        return 'Acoup()'

    def parse_entry(self, entry, now: datetime) -> Item:
        url = URL(entry.link).clean()
        return Item(
            url=url,
            title=entry.title,
            source=Source(url, self.initials),
            created=now,
            modified=now,
        )
