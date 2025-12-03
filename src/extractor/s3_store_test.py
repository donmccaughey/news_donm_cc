from unittest.mock import patch

from .config import S3Creds
from .s3_store import boto3, S3Store


def test_str_and_repr_for_s3_store(monkeypatch):
    s3_creds = S3Creds(
        aws_access_key_id='secret-id',
        aws_secret_access_key='secret-key',
        endpoint_url='https://s3.us-east-1.amazonaws.com',
        region_name='us-east-1'
    )

    with patch('boto3.client'):
        store = S3Store(s3_creds)

        assert str(store) == "S3Store('news.donm.cc', 'news.json')"
        assert repr(store) == "S3Store('news.donm.cc', 'news.json')"
