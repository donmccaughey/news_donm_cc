from .cached_news import CachedNews


class Doc:
    def __init__(self, cached_news: CachedNews, version: str, is_styled: bool):
        self.is_styled = is_styled
        self.version = version

        self.news = cached_news.read()
        self.modified = self.news.modified

        self.counter_reset_item = 0
        self.first_item_index = 0
