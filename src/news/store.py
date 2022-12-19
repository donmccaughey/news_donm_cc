import boto3

from botocore.exceptions import ClientError
from io import BytesIO


class NoStore:
    def get(self) -> str:
        return ''

    def put(self, json: str):
        pass


class S3Store:
    def __init__(self):
        self.bucket = 'news.donm.cc'
        self.object = 'news.json'
        self.s3 = boto3.client('s3')

    def get(self) -> str:
        buffer = BytesIO()
        try:
            self.s3.download_fileobj(self.bucket, self.object, buffer)
            return buffer.getvalue().decode()
        except ClientError as e:
            # TODO: log error
            return ''

    def put(self, json: str):
        buffer = BytesIO(json.encode())
        self.s3.upload_fileobj(buffer, self.bucket, self.object)
