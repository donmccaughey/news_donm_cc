from __future__ import annotations

from argparse import Namespace
from dataclasses import dataclass
from pathlib import Path

from .environ import Environ


@dataclass(frozen=True, slots=True)
class Config:
    cache_dir: Path
    no_store: bool
    read_only: bool
    reddit_private_rss_feed: str

    @classmethod
    def build(cls, options: Namespace, environ: Environ) -> Config:
        return cls(
            cache_dir=options.cache_dir,
            no_store=options.no_store,
            read_only=not environ.read_write,
            reddit_private_rss_feed=environ.reddit_private_rss_feed,
        )
