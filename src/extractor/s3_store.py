import boto3
import sys

from botocore.exceptions import ClientError
from io import BytesIO

from utility import Store
from .config import S3Creds


class S3Store(Store):
    def __init__(
            self,
            s3_creds: S3Creds,
            bucket: str = 'news.donm.cc',
            object: str = 'news.json',
    ):
        self.bucket = bucket
        self.object = object
        self.s3 = boto3.client(
            service_name='s3',
            aws_access_key_id=s3_creds.aws_access_key_id,
            aws_secret_access_key=s3_creds.aws_secret_access_key,
            endpoint_url=s3_creds.endpoint_url,
            region_name=s3_creds.region_name,
        )

    def __repr__(self) -> str:
        return f"S3Store('{self.bucket}', '{self.object}')"

    def read(self) -> str:
        buffer = BytesIO()
        try:
            self.s3.download_fileobj(self.bucket, self.object, buffer)
            return buffer.getvalue().decode()
        except ClientError as e:
            sys.stderr.write(f'{e}\n')
            return ''

    def write(self, contents: str):
        buffer = BytesIO(contents.encode())
        try:
            self.s3.upload_fileobj(buffer, self.bucket, self.object)
        except ClientError as e:
            sys.stderr.write(f'{e}\n')
