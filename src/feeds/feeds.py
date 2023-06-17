import json
from typing import Iterable

from utility.jsontype import JSONList
from .acoup import Acoup
from .charity_wtf import CharityWTF
from .cmake_tags import CMakeTags
from .daring_fireball import DaringFireball
from .hacker_news import HackerNews
from .lobsters import Lobsters
from .reddit import Reddit
from .rust_blog import RustBlog
from .site import Site
from .streetsblog import Streetsblog
from .tilde_news import TildeNews


class Feeds:
    def __init__(self, options: dict):
        self.feeds = [
            Acoup(options),
            CharityWTF(options),
            CMakeTags(options),
            DaringFireball(options),
            HackerNews(options),
            Lobsters(options),
            Reddit(options),
            RustBlog(options),
            Streetsblog(options),
            TildeNews(options),
        ]

    def __iter__(self) -> Iterable[Site]:
        return iter(self.feeds)

    def __len__(self) -> int:
        return len(self.feeds)

    def __repr__(self) -> str:
        site_list = ','.join([repr(site) for site in self.feeds])
        return f'<Feeds: {site_list}>'

    @staticmethod
    def decode(encoded: JSONList, options: dict) -> 'Feeds':
        sites = Feeds(options)
        index = {str(site.feed_url): site for site in sites}
        for encoded_site in encoded:
            site = index.get(encoded_site['feed_url'])
            if site:
                site.etag = encoded_site.get('etag')
                site.last_modified = encoded_site.get('last_modified')
        return sites

    def encode(self) -> JSONList:
        return [site.encode() for site in self.feeds]

    @staticmethod
    def from_json(s: str, options: dict) -> 'Feeds':
        return Feeds.decode(json.loads(s), options) if s else Feeds(options)

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
