from flask.views import MethodView

from .cached_news import CachedNews
from .views import get_numbered_response


class Numbered(MethodView):
    def __init__(self, cached_news: CachedNews, version: str, is_styled: bool):
        self.cached_news = cached_news
        self.version = version
        self.is_styled = is_styled

    def get(self, page_number: int):
        return get_numbered_response(
            self.cached_news, self.version, self.is_styled, page_number
        )
