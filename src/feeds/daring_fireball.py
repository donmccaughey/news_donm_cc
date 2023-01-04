from datetime import datetime

from news import Item, Source, URL
from .site import Site


class DaringFireball(Site):
    def __init__(self):
        super().__init__(
            URL('https://daringfireball.net/feeds/main'),
            'Daring Fireball', 'df'
        )

    def __repr__(self) -> str:
        return 'DaringFireball()'

    def keep_entry(self, entry) -> bool:
        if not self.entry_has_keys(entry, ['link', 'title']):
            return False

        related = first_link_with_rel(entry.links, 'related')
        if related and related.startswith('https://daringfireball.net/feeds/sponsors/'):
            return False

        alternate = first_link_with_rel(entry.links, 'alternate')
        if alternate and alternate.startswith('https://daringfireball.net/thetalkshow/'):
            return False

        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        related = first_link_with_rel(entry.links, 'related')
        alternate = first_link_with_rel(entry.links, 'alternate')
        link = related or alternate or entry.link

        return Item(
            url=URL(link),
            title=entry.title,
            source=Source(URL(link), self.initials),
            created=now,
            modified=now,
        )


def first_link_with_rel(links, rel: str):
    for link in links:
        if link['rel'] == rel:
            return link.href
    return None
