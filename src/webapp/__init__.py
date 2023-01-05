from functools import partial
from pathlib import Path

from flask import Flask

from news import CACHE_DIR, NEWS_FILE
from utility import Cache
from .error_handlers import not_found
from .template_filters import href, iso, utc
from .utility import get_version
from .views import first_page, numbered_page


def create_app(name: str) -> Flask:
    app = Flask(name)

    app.config.from_prefixed_env()

    cache_dir = Path(app.config.get('CACHE_DIR', CACHE_DIR))
    news_cache = Cache(cache_dir / NEWS_FILE)

    version = get_version()

    app.add_url_rule(
        '/', 'first_page',
        partial(first_page, news_cache, version),
        methods=['GET']
    )
    app.add_url_rule(
        '/<int:page_number>', 'numbered_page',
        partial(numbered_page, news_cache, version),
        methods=['GET']
    )

    app.add_template_filter(href)
    app.add_template_filter(iso)
    app.add_template_filter(utc)

    app.jinja_options = {
        'lstrip_blocks': True,
        'trim_blocks': True,
    }

    app.register_error_handler(404, not_found)

    return app