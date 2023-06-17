import json
from typing import Iterable

from news import URL
from utility.jsontype import JSONList
from .acoup import Acoup
from .charity_wtf import CharityWTF
from .cmake_tags import CMakeTags
from .daring_fireball import DaringFireball
from .hacker_news import HackerNews
from .lobsters import Lobsters
from .reddit import Reddit
from .rust_blog import RustBlog
from .feed import Feed
from .streetsblog import Streetsblog
from .tilde_news import TildeNews


class Feeds:
    def __init__(self, feeds: list[Feed] | None = None):
        self.feeds = feeds or []

    def __iter__(self) -> Iterable[Feed]:
        return iter(self.feeds)

    def __len__(self) -> int:
        return len(self.feeds)

    def __repr__(self) -> str:
        feed_list = ','.join([repr(feed) for feed in self.feeds])
        return f'<Feeds: {feed_list}>'

    @staticmethod
    def all(options: dict) -> 'Feeds':
        feeds = [
            Acoup(),
            CharityWTF(),
            CMakeTags(),
            DaringFireball(),
            HackerNews(),
            Lobsters(),
            Reddit(URL(options['reddit_private_rss_feed'])),
            RustBlog(),
            Streetsblog(),
            TildeNews(),
        ]
        return Feeds(feeds)

    @staticmethod
    def decode(encoded: JSONList, options: dict) -> 'Feeds':
        feeds = Feeds.all(options)
        index = {str(feed.name): feed for feed in feeds}
        for encoded_feed in encoded:
            feed = index.get(encoded_feed['name'])
            if feed:
                feed.etag = encoded_feed.get('etag')
                feed.last_modified = encoded_feed.get('last_modified')
        return feeds

    def encode(self) -> JSONList:
        return [feed.encode() for feed in self.feeds]

    @staticmethod
    def from_json(s: str, options: dict) -> 'Feeds':
        return Feeds.decode(json.loads(s), options)

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
