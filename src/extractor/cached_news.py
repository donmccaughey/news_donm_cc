from pathlib import Path

from news import NEWS_FILE, News
from .store import NoStore, S3Store, ReadOnlyStore
from utility import Cache


class CachedNews:
    def __init__(self, cache_dir: Path, no_store: bool, read_only: bool):
        self.store = NoStore() if no_store else S3Store()
        if read_only:
            self.store = ReadOnlyStore(self.store)

        self.cache = Cache(cache_dir / NEWS_FILE)

        self.news = News.from_json(
            self.cache.get() or self.store.get() or News().to_json()
        )

    def __enter__(self) -> News:
        return self.news

    def __exit__(self, exc_type, exc_val, exc_tb):
        json = self.news.to_json()
        self.cache.put(json)
        self.store.put(json)