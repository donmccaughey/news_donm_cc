from .s3_store import S3Store


class FakeS3Client:
    pass


def make_boto3_client_function():
    def fake_client(*args, **kwargs):
        return FakeS3Client()
    return fake_client


def test_str_and_repr_for_s3_store(monkeypatch):
    monkeypatch.setattr('extractor.s3_store.boto3.client', make_boto3_client_function())

    store = S3Store()

    assert str(store) == "S3Store('news.donm.cc', 'news.json')"
    assert repr(store) == "S3Store('news.donm.cc', 'news.json')"
