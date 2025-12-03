from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .environ import Environ
from .options import Options
from .s3_creds import S3Creds


@dataclass(frozen=True, slots=True)
class Config:
    cache_dir: Path
    no_store: bool
    read_only: bool
    reddit_private_rss_feed: str
    s3_creds: S3Creds

    @classmethod
    def build(
        cls, options: Options, environ: Environ, s3_creds: S3Creds
    ) -> Config:
        return cls(
            cache_dir=options.cache_dir,
            no_store=options.no_store,
            read_only=not environ.read_write,
            reddit_private_rss_feed=environ.reddit_private_rss_feed,
            s3_creds=s3_creds,
        )
