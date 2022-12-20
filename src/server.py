from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit

from flask import Flask, render_template

from news import Cache, Items, URL

app = Flask(__name__)
app.config.from_prefixed_env()

news_path = Path(app.config['NEWS_PATH'])
cache = Cache(news_path)


@app.route('/')
def home():
    items = Items.from_json(cache.get() or Items().to_json())
    return render_template('home.html', items=items)


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
