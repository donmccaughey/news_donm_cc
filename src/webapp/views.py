from flask import abort, make_response, redirect, render_template, request, Response

from news import Cache
from .news_page import NewsPage


def news_page(news_cache: Cache, version: str, page_number: int) -> Response:
    news = NewsPage(news_cache, version, page_number)
    if not news.is_valid:
        abort(404)

    html = render_template('news.html', news=news)
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def first_page(news_cache: Cache, version: str) -> Response:
    return news_page(news_cache, version, 1)


def numbered_page(news_cache: Cache, version: str, page_number: int) -> Response:
    if page_number == 1:
        return redirect('/', 308)
    return news_page(news_cache, version, page_number)


def add_cache_control(response: Response):
    if 200 == response.status_code:
        response.cache_control.public = True
        response.cache_control.max_age = 15
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = 15
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True
