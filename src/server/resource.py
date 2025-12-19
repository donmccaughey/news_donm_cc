from dataclasses import dataclass

from flask.views import MethodView

from .cached_news import CachedNews


@dataclass(frozen=True, slots=True)
class Resource(MethodView):
    cached_news: CachedNews
    version: str
    is_styled: bool
