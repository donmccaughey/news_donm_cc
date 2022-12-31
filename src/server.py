from datetime import datetime
from pathlib import Path
from textwrap import dedent

from flask import abort, Flask, make_response, redirect, render_template, request, Response

from news import Cache, News, Page, URL

PAGE_SIZE = 10

app = Flask(__name__)
app.config.from_prefixed_env()
app.jinja_options = {
    'lstrip_blocks': True,
    'trim_blocks': True,
}

cache_dir = Path(app.config.get('CACHE_DIR', Cache.DEFAULT_DIR))
news_cache = Cache(cache_dir / Cache.NEWS_FILE)

version = 'unknown'
version_path = Path('version.txt')
if version_path.exists():
    with version_path.open() as f:
        version = f.read().strip()


@app.route('/', methods=['GET', 'HEAD'])
def home() -> Response:
    news = News.from_json(news_cache.get() or News().to_json())
    page = Page(news, page_number=1, items_per_page=PAGE_SIZE)
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


@app.route('/<int:page_number>', methods=['GET', 'HEAD'])
def numbered_page(page_number: int) -> Response:
    if page_number == 0:
        abort(404)
    if page_number == 1:
        return redirect('/', 308)

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


PAGE_404 = dedent(
    '''
    <!doctype html>
    <html lang=en>
    <link rel=icon href=data:,>
    <meta charset=utf-8>
    <title>News</title>
    <p>404 Not found.
    '''
).strip()


@app.errorhandler(404)
def not_found(e):
    return PAGE_404, 404


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


@app.template_filter()
def iso(value: datetime) -> str:
    return datetime.isoformat(value)


@app.template_filter()
def utc(value: datetime) -> str:
    return value.strftime('%Y-%m-%d %H:%M:%S UTC')


# See "ASCII whitespace" in https://infra.spec.whatwg.org/#ascii-whitespace
ASCII_WHITESPACE = {
    '\t',  # tab
    '\n',  # new line
    '\f',  # form feed
    '\r',  # carriage return
    ' ',
}

# See "Unquoted attribute value syntax" in section 13.1.2.3 "Attributes" of
# https://html.spec.whatwg.org/multipage/syntax.html#attributes-2
SPECIAL_CHARS = ASCII_WHITESPACE | {
    '"',
    "'",
    '=',
    '<',
    '>',
    '`',
}


# TODO: unify with gen/markup/attributes.py
@app.template_filter()
def href(url: URL) -> str:
    href = str(url)
    if href == '':
        return "''"

    chars = set(href)

    if "'" in chars:
        if '"' in chars:
            href = href.replace('"', '&quot;')
        return f'"{href}"'

    if chars & SPECIAL_CHARS:
        return f"'{href}'"

    return href
