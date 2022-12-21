from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, make_response, render_template, request, Response

from news import Cache, News, URL

app = Flask(__name__)
app.config.from_prefixed_env()

news_path = Path(app.config['NEWS_PATH'])
cache = Cache(news_path)


@app.route('/', methods=['GET', 'HEAD'])
def home() -> Response:
    news = News.from_json(cache.get() or News().to_json())
    response = make_response(render_template('home.html', news=news))

    response.add_etag()
    response.last_modified = news.modified

    response.make_conditional(request)

    if 200 == response.status_code:
        now = datetime.now(timezone.utc)
        age = now - news.modified
        five_min = timedelta(minutes=5)
        max_age = five_min - age if age < five_min else timedelta(seconds=15)

        response.cache_control.public = True
        response.cache_control.max_age = max_age.seconds
        response.cache_control.must_revalidate = True
        response.cache_control.s_maxage = max_age.seconds
        response.cache_control.proxy_revalidate = True
        response.cache_control.immutable = True

    return response


@app.template_filter()
def iso(value: datetime) -> str:
    return datetime.isoformat(value)


@app.template_filter()
def utc(value: datetime) -> str:
    return value.strftime('%Y-%m-%d %H:%M:%S UTC')


@app.template_filter()
def domain(value: URL) -> str:
    parts = urlsplit(value.url)
    hostname_parts = parts.hostname.split('.')
    if len(hostname_parts) > 2 and 'www' == hostname_parts[0]:
        del hostname_parts[0]
    hostname = '.'.join(hostname_parts)
    if 'github.com' == hostname:
        if not parts.path:
            return hostname
        path_parts = Path(parts.path).parts
        if not path_parts:
            return hostname
        if not '/' == path_parts[0]:
            return hostname
        if not len(path_parts) > 2:
            return hostname
        return hostname + '/' + path_parts[1]
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

    return href + ' ' if href.endswith('/') else href
