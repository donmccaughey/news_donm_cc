import json
from typing import cast, Iterable, Iterator

from news.url import URL
from serialize import Encodable, JSONDict, JSONList, Serializable
from .aggregator import Aggregator
from .daring_fireball import DaringFireball
from .reddit import Reddit
from .feed import Feed
from .streetsblog import Streetsblog


class Feeds(Encodable, Iterable[Feed], Serializable):
    @staticmethod
    def all(reddit_url: URL) -> 'Feeds':
        feeds = [
            Aggregator(
                'Hacker News',
                'hn',
                URL('https://news.ycombinator.com/rss'),
            ),
            Aggregator(
                'Lobsters',
                'lob',
                URL('https://lobste.rs/rss'),
            ),
            Aggregator(
                'tilde.news',
                '~n',
                URL('https://tilde.news/rss'),
            ),
            Aggregator(
                'Two Stop Bits',
                'tsb',
                URL('https://twostopbits.com/rss'),
            ),
            Feed(
                'A Collection of Unmitigated Pedantry',
                'acoup',
                URL('https://acoup.blog/feed/'),
            ),
            Feed(
                'charity.wtf',
                'cw',
                URL('https://charity.wtf/feed/'),
            ),
            Feed(
                'Molly White',
                'mw',
                URL('https://newsletter.mollywhite.net/feed'),
            ),
            Feed(
                'rust-lang.org',
                'rl',
                URL('https://blog.rust-lang.org/feed.xml'),
            ),
            DaringFireball(),
            Reddit(reddit_url),
            Streetsblog(),
        ]
        return Feeds(feeds)

    def __init__(self, feeds: list[Feed] | None = None):
        self.feeds: dict[Feed, Feed] = {feed: feed for feed in feeds} if feeds else {}

    def __iter__(self) -> Iterator[Feed]:
        return iter(self.feeds.keys())

    def __len__(self) -> int:
        return len(self.feeds)

    def __repr__(self) -> str:
        feed_list = ','.join([repr(feed) for feed in self.feeds.keys()])
        return f'<Feeds: {feed_list}>'

    def update_from(self, other: 'Feeds'):
        for feed in other:
            if feed in self.feeds:
                self.feeds[feed].update_from(feed)

    @staticmethod
    def decode(encoded: JSONDict | JSONList) -> 'Feeds':
        encoded = cast(JSONList, encoded)
        feeds = [Feed.decode(cast(JSONDict, feed)) for feed in encoded]
        return Feeds(feeds)

    def encode(self) -> JSONList:
        return [feed.encode() for feed in self.feeds]

    @staticmethod
    def from_json(s: str) -> 'Feeds':
        return Feeds.decode(json.loads(s))

    def to_json(self) -> str:
        return json.dumps(self.encode(), indent='\t')
