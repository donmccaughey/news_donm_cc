from news import URL
from .feed import Feed


class Streetsblog(Feed):
    def __init__(self):
        super().__init__(
            'Streetsblog SF',
            'sb',
            URL('https://sf.streetsblog.org/feed/'),
        )

    def __repr__(self) -> str:
        return 'Streetsblog()'

    def is_entry_valid(self, entry: dict) -> bool:
        return self.entry_has_keys(entry, ['category', 'link', 'title'])

    def keep_entry(self, entry) -> bool:
        return "Today's Headlines" in entry.category
