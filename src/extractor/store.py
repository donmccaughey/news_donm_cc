from abc import ABC, abstractmethod

import boto3
import sys

from botocore.exceptions import ClientError
from io import BytesIO


class Store(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, contents: str):
        pass


class NoStore(Store):
    def __repr__(self) -> str:
        return 'NoStore()'

    def read(self) -> str:
        return ''

    def write(self, contents: str):
        pass


class ReadOnlyStore(Store):
    def __init__(self, store):
        self.store = store

    def __repr__(self) -> str:
        return f'ReadOnlyStore({repr(self.store)})'

    def read(self) -> str:
        return self.store.read()

    def write(self, contents: str):
        pass


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
