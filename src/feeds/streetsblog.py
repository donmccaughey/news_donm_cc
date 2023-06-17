from news import URL
from .feed import Feed


class Streetsblog(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            URL('https://sf.streetsblog.org/feed/'),
            'Streetsblog SF',
            'sb',
        )

    def __repr__(self) -> str:
        return 'Streetsblog()'

    def is_entry_valid(self, entry: dict) -> bool:
        return self.entry_has_keys(entry, ['category', 'link', 'title'])

    def keep_entry(self, entry) -> bool:
        return "Today's Headlines" in entry.category
