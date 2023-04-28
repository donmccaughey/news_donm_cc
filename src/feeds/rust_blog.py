from datetime import datetime

from news import Item, Source, URL
from .site import Site


class RustBlog(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://blog.rust-lang.org/feed.xml'),
            'rust-lang.org', 'rl',
        )

    def __repr__(self) -> str:
        return 'RustBlog()'

    def parse_entry(self, entry, now: datetime) -> Item:
        url = URL(entry.link).clean()
        return Item(
            url=url,
            title=entry.title,
            source=Source(url, self.initials),
            created=now,
            modified=now,
        )
