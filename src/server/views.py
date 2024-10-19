from typing import cast
from flask import abort, make_response, redirect, request, Response

from .cached_news import CachedNews
from .doc import Doc
from .news_doc import NewsDoc
from .search_doc import SearchDoc
from .site_doc import SiteDoc
from .sites_doc import SitesDoc


def get_home_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
) -> Response:
    if 'q' in request.args:
        return get_search_response(
            cached_news, version, is_styled, request.args['q']
        )
    else:
        return get_news_response(cached_news, version, is_styled, 1)


def get_numbered_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    if page_number == 1:
        return cast(Response, redirect('/', 308))
    return get_news_response(cached_news, version, is_styled, page_number)


def get_news_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    doc = NewsDoc(
        cached_news,
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
    return make_doc_response(SearchDoc(cached_news, version, is_styled, query))


def get_site_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        identity: str,
) -> Response:
    return make_doc_response(SiteDoc(cached_news, version, is_styled, identity))


def get_sites_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
) -> Response:
    return make_doc_response(SitesDoc(cached_news, version, is_styled))


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
