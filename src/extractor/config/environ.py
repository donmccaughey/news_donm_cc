from __future__ import annotations

import os

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Environ:
    read_write: bool
    reddit_private_rss_feed: str

    @classmethod
    def read(cls) -> Environ:
        return cls(
            read_write = _environ_is_true('EXTRACTOR_READ_WRITE'),
            reddit_private_rss_feed = os.environ['REDDIT_PRIVATE_RSS_FEED'],
        )


def _environ_is_true(name: str) -> bool:
    return (
        name in os.environ
        and os.environ[name].lower() in ['true', 'yes', '1']
    )
