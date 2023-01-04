from datetime import datetime

from news import Item, Source, URL
from .site import Site


class Streetsblog(Site):
    def __init__(self):
        super().__init__(
            URL('https://sf.streetsblog.org/feed/'),
            'Streetsblog SF', 'sb'
        )

    def __repr__(self) -> str:
        return 'Streetsblog()'

    def keep_entry(self, entry) -> bool:
        if not self.entry_has_keys(entry, ['link', 'title', 'category']):
            return False
        return "Today's Headlines" in entry.category

    def parse_entry(self, entry, now: datetime) -> Item:
        return Item(
            url=URL(entry.link),
            title=entry.title,
            source=Source(URL(entry.link), self.initials),
            created=now,
            modified=now,
        )
