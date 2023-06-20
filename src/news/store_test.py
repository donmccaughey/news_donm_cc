from .store import NoStore
from .store import S3Store


def test_str_and_repr_for_no_store():
    store = NoStore()

    assert str(store) == 'NoStore()'
    assert repr(store) == 'NoStore()'


class FakeS3Client:
    def __init__(self):
        pass


def make_boto3_client_function():
    def fake_client(*args, **kwargs):
        return FakeS3Client()
    return fake_client


def test_str_and_repr_for_s3_store(monkeypatch):
    monkeypatch.setattr('news.store.boto3.client', make_boto3_client_function())

    store = S3Store()

    assert str(store) == "S3Store('news.donm.cc', 'news.json')"
    assert repr(store) == "S3Store('news.donm.cc', 'news.json')"
