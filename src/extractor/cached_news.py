from pathlib import Path

from news import NEWS_FILE, News
from utility import CachedFile, NoStore, ReadOnlyStore
from .s3_store import S3Store


class CachedNews:
    def __init__(self, cache_dir: Path, no_store: bool, read_only: bool):
        self.store = NoStore() if no_store else S3Store()
        if read_only:
            self.store = ReadOnlyStore(self.store)

        self.cached_file = CachedFile(cache_dir / NEWS_FILE)

        self.news = News.from_json(
            self.cached_file.read() or self.store.read() or News().to_json()
        )

    def __enter__(self) -> News:
        return self.news

    def __exit__(self, exc_type, exc_val, exc_tb):
        contents = self.news.to_json()
        self.cached_file.write(contents)
        self.store.write(contents)
