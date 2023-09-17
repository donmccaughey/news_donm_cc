from pathlib import Path

from news import News
from utility import CachedFile


class CachedNews:
    def __init__(self, path: Path):
        self.cached_file = CachedFile(path)
        self.news = read_news(self.cached_file)

    def read(self) -> News:
        if self.cached_file.is_invalid():
            self.news = read_news(self.cached_file)
        return self.news


def read_news(cached_file: CachedFile):
    return News.from_json(cached_file.read() or News().to_json())
