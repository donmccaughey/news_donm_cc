from collections.abc import Buffer
from io import BytesIO
from typing import BinaryIO, cast, Iterable

from pytest import raises

from .body import body_repr, is_body_readable


def test_body_repr() -> None:
    no_body = None
    assert body_repr(no_body) == ''

    buffer = '42'.encode()
    assert body_repr(buffer) == '<Buffer: 2 bytes>'

    bytes_io = MyBytesIO('42'.encode())
    assert body_repr(bytes_io) == '<MyBytesIO object>'

    binary_io = MyBinaryIO()
    assert body_repr(binary_io) == '<MyBinaryIO object>'

    unexpected = cast(BinaryIO, cast(object, 42))
    with raises(RuntimeError):
        body_repr(unexpected)


def test_is_body_readable() -> None:
    assert is_body_readable(MyBinaryIO())
    assert is_body_readable(MyBytesIO('42'.encode()))

    assert not is_body_readable('42'.encode())


class MyBytesIO(BytesIO):
    def __repr__(self) -> str:
        return '<MyBytesIO object>'


class MyBinaryIO(BinaryIO):
    def __enter__(self):
        pass

    def __exit__(self, type, value, traceback):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass

    def __repr__(self) -> str:
        return '<MyBinaryIO object>'

    def close(self):
        pass

    def fileno(self):
        pass

    def flush(self):
        pass

    def isatty(self):
        pass

    def read(self, n=-1):
        pass

    def readable(self):
        pass

    def readline(self, limit=-1):
        pass

    def readlines(self, hint=-1):
        pass

    def seek(self, offset, whence=0):
        pass

    def seekable(self):
        pass

    def tell(self):
        pass

    def truncate(self, size=None):
        pass

    def writable(self):
        pass

    def write(self, s: Buffer | bytes) -> int:
        return 0

    def writelines(self, lines: Iterable[Buffer]) -> None:
        pass
