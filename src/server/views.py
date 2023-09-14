from flask import abort, make_response, redirect, render_template, request, Response

from utility import Cache
from .news_page import NewsPage
from .site_page import SitePage
from .sites_page import SitesPage


def news_page(
        news_cache: Cache,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    news = NewsPage(news_cache, version, is_styled, page_number)
    if not news.is_valid:
        abort(404)

    html = render_template('news.html', news=news)
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def first_page(
        news_cache: Cache,
        version: str,
        is_styled: bool,
) -> Response:
    return news_page(news_cache, version, is_styled, 1)


def numbered_page(
        news_cache: Cache,
        version: str,
        is_styled: bool,
        page_number: int,
) -> Response:
    if page_number == 1:
        return redirect('/', 308)
    return news_page(news_cache, version, is_styled, page_number)


def site_page(
        news_cache: Cache,
        version: str,
        is_styled: bool,
        identity: str,
) -> Response:
    site = SitePage(news_cache, version, is_styled, identity)
    html = render_template('site.html', news=site)
    response = make_response(html)

    response.add_etag()
    response.last_modified = site.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def sites_page(
        news_cache: Cache,
        version: str,
        is_styled: bool,
) -> Response:
    sites = SitesPage(news_cache, version, is_styled)
    html = render_template('sites.html', news=sites)
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
