from functools import partial
from pathlib import Path

from flask import Flask

from news import CACHE_DIR, NEWS_FILE
from utility import iso, utc
from .cached_news import CachedNews
from .error_handlers import not_found
from .template_filters import href
from .utility import get_version
from .views import first_page, numbered_page, site_page, sites_page


def create_app() -> Flask:
    app = Flask('server')

    app.config.from_prefixed_env()

    cache_dir = Path(app.config.get('CACHE_DIR', CACHE_DIR))
    cached_news = CachedNews(cache_dir / NEWS_FILE)

    version = get_version()
    is_styled = True

    app.add_url_rule(
        '/', 'first_page',
        partial(first_page, cached_news, version, is_styled),
        methods=['GET']
    )
    app.add_url_rule(
        '/<int:page_number>', 'numbered_page',
        partial(numbered_page, cached_news, version, is_styled),
        methods=['GET']
    )
    app.add_url_rule(
        '/site/<path:identity>', 'site_page',
        partial(site_page, cached_news, version, is_styled),
        methods=['GET']
    )

    app.add_url_rule(
        '/sites', 'sites_page',
        partial(sites_page, cached_news, version, is_styled),
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
