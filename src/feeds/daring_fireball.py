from datetime import datetime
from urllib.parse import parse_qsl, urlsplit

from news import Item, Source, URL
from .feed import Feed


class DaringFireball(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'Daring Fireball',
            'df',
            URL('https://daringfireball.net/feeds/main')
        )

    def __repr__(self) -> str:
        return 'DaringFireball()'

    def keep_entry(self, entry) -> bool:
        related = first_link_with_rel(entry.links, 'related')
        if related:
            _, netloc, path, _, _ = urlsplit(related)
            if netloc == 'daringfireball.net' and path.startswith('/feeds/sponsors/'):
                return False

        alternate = first_link_with_rel(entry.links, 'alternate')
        if alternate:
            _, netloc, path, query, _ = urlsplit(alternate)

            if netloc == 'dithering.fm':
                return False

            if netloc == 'daringfireball.net':
                if path.startswith('/thetalkshow/'):
                    return False
                if path.startswith('/feeds/sponsors/'):
                    return False

            parameters = parse_qsl(query)
            if ('utm_source', 'daringfireball') in parameters:
                return False

        return True

    def parse_entry(self, entry, now: datetime) -> Item:
        related = first_link_with_rel(entry.links, 'related')
        alternate = first_link_with_rel(entry.links, 'alternate')
        link = related or alternate or entry.link

        url = URL(link)
        return Item(
            url=url,
            title=entry.title,
            sources=[Source(url, self.initials)],
            created=now,
            modified=now,
        )


def first_link_with_rel(links, rel: str):
    for link in links:
        if link['rel'] == rel:
            return link.href
    return None
