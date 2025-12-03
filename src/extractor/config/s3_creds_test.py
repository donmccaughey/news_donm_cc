from unittest.mock import Mock, patch

from pytest import raises

from .s3_creds import boto3, S3Creds


def test_missing_region_name() -> None:
    with patch('boto3.Session') as Session:
        session = Session.return_value = Mock()
        session.region_name = None
        with raises(AssertionError):
            S3Creds.for_aws()


def test_missing_credentials() -> None:
    with patch('boto3.Session') as Session:
        session = Session.return_value = Mock()
        session.region_name = 'us-east-1'
        session.get_credentials = Mock(return_value=None)
        with raises(AssertionError):
            S3Creds.for_aws()


def test_for_aws() -> None:
    creds = S3Creds.for_aws()

    assert creds.aws_access_key_id
    assert creds.aws_secret_access_key
    assert creds.endpoint_url
    assert creds.region_name
