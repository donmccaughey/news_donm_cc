from .headers import Headers, headers_repr


def test_headers_repr() -> None:
    headers: Headers = {}
    assert headers_repr(headers) == []

    headers = {'Content-Type': 'text/plain'}
    expected = [
        'Content-Type: text/plain',
    ]
    assert headers_repr(headers) == expected

    headers = {
        'Content-Type': 'text/plain',
        'Content-Length': '42',
    }
    expected = [
        'Content-Length: 42',
        'Content-Type: text/plain',
    ]
    assert headers_repr(headers) == expected
