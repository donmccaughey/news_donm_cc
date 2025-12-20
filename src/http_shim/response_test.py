from .response import Response


def test_start_line() -> None:
    response = Response(
        status_code=200,
        reason_phrase='OK',
        headers={'Content-Type': 'text/plain'},
        body='Hello, world!',
    )
    assert response.start_line == 'HTTP/1.1 200 OK'


def test_str() -> None:
    response = Response(
        status_code=200,
        reason_phrase='OK',
        headers={
            'Content-Type': 'text/plain',
            'Content-Length': '6',
        },
        body='Hello!',
    )

    assert str(response) == (
        'HTTP/1.1 200 OK\r\n'
        'Content-Length: 6\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        'Hello!'
    )
