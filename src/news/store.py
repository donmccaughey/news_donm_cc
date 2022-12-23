import boto3
import sys

from botocore.exceptions import ClientError
from io import BytesIO


class NoStore:
    def __repr__(self) -> str:
        return 'NoStore()'

    def get(self) -> str:
        return ''

    def put(self, json: str):
        pass


class S3Store:
    def __init__(self, bucket: str = 'news.donm.cc', object: str = 'news.json'):
        self.bucket = bucket
        self.object = object
        self.s3 = boto3.client('s3')

    def __repr__(self) -> str:
        return f"S3Store('{self.bucket}', '{self.object}')"

    def get(self) -> str:
        buffer = BytesIO()
        try:
            self.s3.download_fileobj(self.bucket, self.object, buffer)
            return buffer.getvalue().decode()
        except ClientError as e:
            sys.stderr.write(f'{e}\n')
            return ''

    def put(self, json: str):
        buffer = BytesIO(json.encode())
        try:
            self.s3.upload_fileobj(buffer, self.bucket, self.object)
        except ClientError as e:
            sys.stderr.write(f'{e}\n')
