from collections.abc import Buffer
from io import BufferedIOBase
from typing import BinaryIO


type Body = Buffer | BinaryIO


def body_repr(body: Body | None) -> str:
    if body is None:
        return ''
    elif isinstance(body, Buffer):
        buffer = memoryview(body)
        return f'<Buffer: {buffer.nbytes} bytes>'
    elif is_body_readable(body):
        return repr(body)
    else:
        raise RuntimeError(f'Unexpected body {body!r}')


def is_body_readable(body: Body) -> bool:
    return isinstance(body, BinaryIO) or isinstance(body, BufferedIOBase)
