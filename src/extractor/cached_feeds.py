from pathlib import Path

from feeds import Feeds
from news.url import URL
from utility import CachedFile


class CachedFeeds:
    def __init__(self, cache_dir: Path, reddit_private_rss_feed: str):
        self.feeds = Feeds.all(URL(reddit_private_rss_feed))
        self.cached_file = CachedFile(cache_dir / 'feeds.json')
        cached_feeds = Feeds.from_json(self.cached_file.read() or Feeds().to_json())
        self.feeds.update_from(cached_feeds)

    def __enter__(self) -> Feeds:
        return self.feeds

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cached_file.write(self.feeds.to_json())
