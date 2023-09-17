from pathlib import Path

from .cached_file import CachedFile


def test_str_and_repr():
    cache = CachedFile(Path('/tmp/news.json'))

    assert str(cache) == "CachedFile(Path('/tmp/news.json'))"
    assert repr(cache) == "CachedFile(Path('/tmp/news.json'))"
