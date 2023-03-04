import json
from typing import Iterable

from .acoup import Acoup
from .charity_wtf import CharityWTF
from .daring_fireball import DaringFireball
from .hacker_news import HackerNews
from .site import Site
from .streetsblog import Streetsblog
from .tilde_news import TildeNews


class Sites:
    def __init__(self):
        self.sites = [
            Acoup(),
            CharityWTF(),
            DaringFireball(),
            HackerNews(),
            Streetsblog(),
            TildeNews(),
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
