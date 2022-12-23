from .source import Source
from .url import URL


def test_str_and_repr():
    source = Source(URL('https://news.ycombinator.com/rss'))

    assert str(source) == 'https://news.ycombinator.com/rss'
    assert repr(source) == "Source(URL('https://news.ycombinator.com/rss'))"
