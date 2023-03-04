from datetime import datetime

from news import Item, Source, URL
from .site import Site


class CMakeTags(Site):
    def __init__(self):
        super().__init__(
            URL('https://gitlab.kitware.com/cmake/cmake/-/tags?format=atom'),
            'kitware.com', 'cm'
        )

    def __repr__(self) -> str:
        return 'CMakeTags()'

    def parse_entry(self, entry, now: datetime) -> Item:
        url = URL(entry.link).clean()
        return Item(
            url=url,
            title=entry.title,
            source=Source(url, self.initials),
            created=now,
            modified=now,
        )
