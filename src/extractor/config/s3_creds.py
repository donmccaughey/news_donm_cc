from __future__ import annotations

from dataclasses import dataclass

import boto3


@dataclass(frozen=True, slots=True)
class S3Creds:
    aws_access_key_id: str
    aws_secret_access_key: str
    endpoint_url: str
    region_name: str

    @classmethod
    def for_aws(cls) -> S3Creds:
        """Read AWS configuration and credentials using a boto3 Session.

        See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html
        for AWS credential sources and search order.
        """
        session = boto3.Session()
        assert session.region_name

        credentials = session.get_credentials()
        assert credentials

        return cls(
            aws_access_key_id=credentials.access_key,
            aws_secret_access_key=credentials.secret_key,
            endpoint_url=_make_aws_s3_endpoint_url(session.region_name),
            region_name=session.region_name,
        )


def _make_aws_s3_endpoint_url(region_name: str) -> str:
    # see https://docs.aws.amazon.com/general/latest/gr/rande.html
    # and https://docs.aws.amazon.com/general/latest/gr/s3.html
    return f'https://s3.{region_name}.amazonaws.com'
