from pathlib import Path

from .cache import Cache


def test_str_and_repr():
    cache = Cache(Path('/tmp/news.json'))

    assert str(cache) == "Cache(Path('/tmp/news.json'))"
    assert repr(cache) == "Cache(Path('/tmp/news.json'))"
