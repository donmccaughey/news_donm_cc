from pathlib import Path

from flask import Flask

from news import CACHE_DIR, NEWS_FILE
from utility import iso, utc
from .cached_news import CachedNews
from .error_handlers import not_found
from .home import Home
from .numbered import Numbered
from .site import Site
from .sites import Sites
from .template_filters import href
from .utility import get_version


def create_app() -> Flask:
    app = Flask('server')

    app.config.from_prefixed_env()

    cache_dir = Path(app.config.get('CACHE_DIR', CACHE_DIR))
    cached_news = CachedNews(cache_dir / NEWS_FILE)

    version = get_version()
    is_styled = True

    app.add_url_rule(
        '/',
        view_func=Home.as_view('home', cached_news, version, is_styled)
    )
    app.add_url_rule(
        '/<int:page_number>',
        view_func=Numbered.as_view('numbered', cached_news, version, is_styled)
    )
    app.add_url_rule(
        '/site/<path:identity>',
        view_func=Site.as_view('site', cached_news, version, is_styled),
    )
    app.add_url_rule(
        '/sites',
        view_func=Sites.as_view('sites', cached_news, version, is_styled),
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
