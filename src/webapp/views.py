from flask import abort, make_response, redirect, render_template, request, Response

from news import Cache, News, Page


PAGE_SIZE = 10


def news_page(news_cache: Cache, version: str, page_number: int) -> Response:
    news = News.from_json(news_cache.get() or News().to_json())
    page = Page(news, page_number=page_number, items_per_page=PAGE_SIZE)
    if page.number > page.count:
        abort(404)

    html = render_template(
        'news.html', news=news, page=page, item_count=page.begin,
        next_url=next_url(page), previous_url=previous_url(page),
        first_url=first_url(page), last_url=last_url(page),
        version=version
    )
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def first_page(news_cache: Cache, version: str) -> Response:
    return news_page(news_cache, version, 1)


def numbered_page(news_cache: Cache, version: str, page_number: int) -> Response:
    if page_number < 1:
        abort(404)
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


def first_url(page: Page) -> str | None:
    if page.number > 1:
        return './'
    else:
        return None


def last_url(page: Page) -> str | None:
    last_page = page.last
    if last_page:
        return f'./{last_page.number}'
    else:
        return None


def next_url(page: Page) -> str | None:
    next_page = page.next
    if next_page:
        return f'./{next_page.number}'
    else:
        return None


def previous_url(page: Page) -> str | None:
    previous_page = page.previous
    if previous_page:
        if previous_page.number == 1:
            return './'
        else:
            return f'./{previous_page.number}'
    else:
        return None
