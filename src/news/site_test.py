from .site import Site
from .url import URL


def test_str_and_repr():
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert str(site) == 'Hacker News'
    assert repr(site) == "Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')"
