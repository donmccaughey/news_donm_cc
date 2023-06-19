from pathlib import Path

from feeds import Feeds
from news import URL
from utility import Cache


class CachedFeeds:
    def __init__(self, cache_dir: Path, reddit_private_rss_feed: str):
        self.feeds = Feeds.all(URL(reddit_private_rss_feed))
        self.cache = Cache(cache_dir / 'feeds.json')
        cached_feeds = Feeds.from_json(self.cache.get() or Feeds().to_json())
        self.feeds.update_from(cached_feeds)

    def __enter__(self) -> Feeds:
        return self.feeds

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cache.put(self.feeds.to_json())
