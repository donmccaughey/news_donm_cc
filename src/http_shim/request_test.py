from .request import Request


def test_start_line() -> None:
    request = Request(
        method='DELETE',
        base_url='https://example.com',
        route='/a/thing',
        headers={'Accept': 'text/html'},
    )
    assert request.start_line == 'DELETE /a/thing HTTP/1.1'


def test_url() -> None:
    request = Request(
        method='GET',
        base_url='https://example.com',
        route='/some/thing',
        headers={'Accept': 'text/html'},
    )
    assert request.url == 'https://example.com/some/thing'


def test_str() -> None:
    request = Request(
        method='POST',
        base_url='https://example.com',
        route='/update',
        headers={
            'Accept': 'text/html',
            'Content-Type': 'text/plain'
        },
        body='foobar',
    )

    assert str(request) == (
        'POST /update HTTP/1.1\r\n'
        'Accept: text/html\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        'foobar'
    )
