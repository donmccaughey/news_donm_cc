import boto3
import sys

from botocore.exceptions import ClientError
from io import BytesIO

from utility import Store


class S3Store(Store):
    def __init__(self, bucket: str = 'news.donm.cc', object: str = 'news.json'):
        self.bucket = bucket
        self.object = object
        self.s3 = boto3.client('s3')

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
