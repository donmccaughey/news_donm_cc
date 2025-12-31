from typing import Mapping


type Headers = Mapping[str, str]


def headers_repr(headers: Headers) -> list[str]:
    return [
        f'{name}: {value}' for name, value in sorted(headers.items())
    ]
