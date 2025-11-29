from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Config:
    cache_dir: Path
    no_store: bool
    read_only: bool
    reddit_private_rss_feed: str

    @classmethod
    def build(cls, options: Namespace):
        return cls(
            cache_dir=options.cache_dir,
            no_store=options.no_store,
            read_only=options.read_only,
            reddit_private_rss_feed=options.reddit_private_rss_feed,
        )
