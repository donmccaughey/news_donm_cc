from dataclasses import dataclass

from flask import make_response, request, Response
from flask.views import MethodView

from .cached_news import CachedNews
from .doc import Doc


@dataclass(frozen=True, slots=True)
class Resource(MethodView):
    cached_news: CachedNews
    version: str
    is_styled: bool

    @staticmethod
    def make_doc_response(doc: Doc) -> Response:
        response = make_response(doc.get_representation())

        response.add_etag()
        response.last_modified = doc.modified

        response.make_conditional(request)
        _add_cache_control(response)
        response.vary.add('Accept')

        return response


def _add_cache_control(response: Response):
    if 200 == response.status_code:
        response.cache_control.public = True
        response.cache_control.max_age = 15
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = 15
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True
