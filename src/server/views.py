from typing import cast
from flask import abort, make_response, redirect, render_template, request, Response

from .cached_news import CachedNews
from .news_doc import NewsDoc
from .search_doc import SearchDoc
from .site_page import SitePage
from .sites_page import SitesPage


ACCEPTED = ['application/json', 'text/html']


def get_news_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    accepts_json = 'application/json' == request.accept_mimetypes.best_match(ACCEPTED)
    if accepts_json:
        items_per_page = 100
        full_urls = True
    else:
        items_per_page = 10
        full_urls = False

    doc = NewsDoc(
        cached_news, version, is_styled, page_number, items_per_page, full_urls
    )
    if not doc.is_valid:
        abort(404)

    representation = (
        doc.to_json() if accepts_json
        else render_template('news.html', doc=doc)
    )
    response = make_response(representation)

    response.add_etag()
    response.last_modified = doc.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def get_first_news_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
) -> Response:
    if 'q' in request.args:
        return get_search_response(cached_news, version, is_styled, request.args['q'])
    else:
        return get_news_response(cached_news, version, is_styled, 1)


def get_numbered_news_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    if page_number == 1:
        return cast(Response, redirect('/', 308))
    return get_news_response(cached_news, version, is_styled, page_number)


def get_search_response(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        query: str,
):
    search = SearchDoc(cached_news, version, is_styled, query)
    html = render_template('search.html', doc=search)
    response = make_response(html)

    response.add_etag()
    response.last_modified = search.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def site_doc(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
        identity: str,
) -> Response:
    site = SitePage(cached_news, version, is_styled, identity)
    html = render_template('site.html', doc=site)
    response = make_response(html)

    response.add_etag()
    response.last_modified = site.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def sites_doc(
        cached_news: CachedNews,
        version: str,
        is_styled: bool,
) -> Response:
    sites = SitesPage(cached_news, version, is_styled)
    html = render_template('sites.html', doc=sites)
    response = make_response(html)

    response.add_etag()
    response.last_modified = sites.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def add_cache_control(response: Response):
    if 200 == response.status_code:
        response.cache_control.public = True
        response.cache_control.max_age = 15
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = 15
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True
