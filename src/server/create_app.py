from functools import partial
from pathlib import Path

from flask import Flask

from news import CACHE_DIR, NEWS_FILE
from utility import iso, utc
from .cached_news import CachedNews
from .error_handlers import not_found
from .template_filters import href
from .utility import get_version
from .views import get_first_news_doc, get_numbered_news_doc, site_doc, sites_doc


def create_app() -> Flask:
    app = Flask('server')

    app.config.from_prefixed_env()

    cache_dir = Path(app.config.get('CACHE_DIR', CACHE_DIR))
    cached_news = CachedNews(cache_dir / NEWS_FILE)

    version = get_version()
    is_styled = True

    app.add_url_rule(
        '/', 'first_news',
        partial(get_first_news_doc, cached_news, version, is_styled),
        methods=['GET']
    )
    app.add_url_rule(
        '/<int:page_number>', 'numbered_news',
        partial(get_numbered_news_doc, cached_news, version, is_styled),
        methods=['GET']
    )
    app.add_url_rule(
        '/site/<path:identity>', 'site',
        partial(site_doc, cached_news, version, is_styled),
        methods=['GET']
    )
    app.add_url_rule(
        '/sites', 'sites',
        partial(sites_doc, cached_news, version, is_styled),
        methods=['GET']
    )

    app.jinja_options = {
        'lstrip_blocks': True,
        'trim_blocks': True,
    }

    app.add_template_filter(href)
    app.add_template_filter(iso)
    app.add_template_filter(utc)

    app.register_error_handler(404, not_found)

    return app
