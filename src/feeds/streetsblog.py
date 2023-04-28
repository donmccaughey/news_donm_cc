from datetime import datetime

from news import Item, Source, URL
from .site import Site


class Streetsblog(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://sf.streetsblog.org/feed/'),
            'Streetsblog SF', 'sb',
        )

    def __repr__(self) -> str:
        return 'Streetsblog()'

    def keep_entry(self, entry) -> bool:
        if not self.entry_has_keys(entry, ['link', 'title', 'category']):
            return False
        return "Today's Headlines" in entry.category

    def parse_entry(self, entry, now: datetime) -> Item:
        url = URL(entry.link).clean()
        return Item(
            url=url,
            title=entry.title,
            source=Source(url, self.initials),
            created=now,
            modified=now,
        )
