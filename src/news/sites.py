import json
from typing import Iterable

from .site import Acoup, DaringFireball, HackerNews, Site, Streetsblog


class Sites:
    def __init__(self):
        self.sites = [
            Acoup(),
            DaringFireball(),
            HackerNews(),
            Streetsblog(),
        ]

    def __iter__(self) -> Iterable[Site]:
        return iter(self.sites)

    def __len__(self) -> int:
        return len(self.sites)

    def __repr__(self) -> str:
        site_list = ','.join([repr(site) for site in self.sites])
        return f'<Sites: {site_list}>'

    @staticmethod
    def decode(encoded: list[dict[str, str]]) -> 'Sites':
        sites = Sites()
        index = {str(site.feed_url): site for site in sites}
        for encoded_site in encoded:
            site = index.get(encoded_site['feed_url'])
            if site:
                site.etag = encoded_site.get('etag')
                site.last_modified = encoded_site.get('last_modified')
        return sites

    def encode(self) -> list[dict[str, str]]:
        return [site.encode() for site in self.sites]

    @staticmethod
    def from_json(s: str) -> 'Sites':
        return Sites.decode(json.loads(s)) if s else Sites()

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
