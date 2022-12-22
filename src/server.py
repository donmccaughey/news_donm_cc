from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, make_response, render_template, request, Response

from news import Cache, News, Page, URL

PAGE_SIZE = 10

app = Flask(__name__)
app.config.from_prefixed_env()

news_path = Path(app.config['NEWS_PATH'])
cache = Cache(news_path)


@app.route('/', methods=['GET', 'HEAD'])
def home() -> Response:
    news = News.from_json(cache.get() or News().to_json())
    page = Page(news, page_number=1, items_per_page=PAGE_SIZE)
    html = render_template(
        'home.html', news=news, page=page, item_count=page.begin,
        next_url=next_url(page), previous_url=previous_url(page),
        first_url=first_url(page), last_url=last_url(page),
    )
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


@app.route('/all', methods=['GET', 'HEAD'])
def all() -> Response:
    news = News.from_json(cache.get() or News().to_json())
    html = render_template('home.html', news=news, page=news, item_count=0)
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


@app.route('/<int:page_number>', methods=['GET', 'HEAD'])
def numbered_page(page_number: int) -> Response:
    news = News.from_json(cache.get() or News().to_json())
    page = Page(news, page_number=page_number, items_per_page=PAGE_SIZE)
    html = render_template(
        'home.html', news=news, page=page, item_count=page.begin,
        next_url=next_url(page), previous_url=previous_url(page),
        first_url=first_url(page), last_url=last_url(page),
    )
    response = make_response(html)

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)
    add_cache_control(response)

    return response


def add_cache_control(response: Response):
    if 200 == response.status_code:
        now = datetime.now(timezone.utc)
        age = now - response.last_modified
        five_min = timedelta(minutes=5)
        max_age = five_min - age if age < five_min else timedelta(seconds=15)

        response.cache_control.public = True
        response.cache_control.max_age = max_age.seconds
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = max_age.seconds
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True


def first_url(page: Page) -> str | None:
    if page.number > 1:
        return '/'
    else:
        return None


def last_url(page: Page) -> str | None:
    last_page = page.last
    if last_page:
        return f'/{last_page.number}'
    else:
        return None


def next_url(page: Page) -> str | None:
    next_page = page.next
    if next_page:
        return f'/{next_page.number}'
    else:
        return None


def previous_url(page: Page) -> str | None:
    previous_page = page.previous
    if previous_page:
        if previous_page.number == 1:
            return '/'
        else:
            return f'/{previous_page.number}'
    else:
        return None


@app.template_filter()
def iso(value: datetime) -> str:
    return datetime.isoformat(value)


@app.template_filter()
def utc(value: datetime) -> str:
    return value.strftime('%Y-%m-%d %H:%M:%S UTC')


@app.template_filter()
def domain(value: URL) -> str:
    parts = urlsplit(value.url)

    hostname = parts.hostname
    path = parts.path

    if 'old.reddit.com' == hostname:
        hostname = 'reddit.com'

    hostname_parts = hostname.split('.')
    if len(hostname_parts) > 2 and 'www' == hostname_parts[0]:
        del hostname_parts[0]
    hostname = '.'.join(hostname_parts)

    if 'github.com' == hostname:
        if not parts.path:
            return hostname
        path_parts = Path(path).parts
        if not path_parts:
            return hostname
        if not '/' == path_parts[0]:
            return hostname
        if not len(path_parts) > 2:
            return hostname
        return hostname + '/' + path_parts[1]
    elif 'reddit.com' == hostname:
        if not parts.path:
            return hostname
        path_parts = Path(path).parts
        if not path_parts:
            return hostname
        if not '/' == path_parts[0]:
            return hostname
        if not len(path_parts) > 2:
            return hostname
        if not 'r' == path_parts[1]:
            return hostname
        return hostname + '/r/' + path_parts[2]
    else:
        return hostname


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
