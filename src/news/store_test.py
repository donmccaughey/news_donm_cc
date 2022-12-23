from .store import NoStore
from .store import S3Store


def test_str_and_repr_for_no_store():
    store = NoStore()

    assert str(store) == 'NoStore()'
    assert repr(store) == 'NoStore()'


def test_str_and_repr_for_s3_store():
    store = S3Store()

    assert str(store) == "S3Store('news.donm.cc', 'news.json')"
    assert repr(store) == "S3Store('news.donm.cc', 'news.json')"
