from flask import abort, make_response, request, Response

from .cached_news import CachedNews
from .doc import Doc
from .news_doc import NewsDoc
from .search_doc import SearchDoc


def get_news_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    doc = NewsDoc(
        cached_news.read(),
        version,
        is_styled,
        request.accept_mimetypes,
        page_number,
    )
    if not doc.page.is_valid:
        abort(404)
    return make_doc_response(doc)


def get_search_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        query: str,
):
    return make_doc_response(
        SearchDoc(cached_news.read(), version, is_styled, query)
    )


def make_doc_response(doc: Doc) -> Response:
    response = make_response(doc.get_representation())

    response.add_etag()
    response.last_modified = doc.modified

    response.make_conditional(request)
    add_cache_control(response)
    response.vary.add('Accept')

    return response


def add_cache_control(response: Response):
    if 200 == response.status_code:
        response.cache_control.public = True
        response.cache_control.max_age = 15
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = 15
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True
