from .message import Message


class MyMessage(Message):
    @property
    def start_line(self) -> str:
        return 'MyMessage Line One'


def test_str() -> None:
    my_message = MyMessage(
        headers={
            'Content-Type': 'text/plain',
            'Content-Length': '2',
        },
        body='foo',
    )

    assert str(my_message) == (
        'MyMessage Line One\r\n'
        'Content-Length: 2\r\n'
        'Content-Type: text/plain\r\n'
        '\r\n'
        'foo'
    )


def test_to_str() -> None:
    my_message = MyMessage(
        headers={
            'Content-Type': 'text/plain',
            'Content-Length': '2',
        },
        body='42',
    )

    assert my_message.to_str('|\n') == (
        'MyMessage Line One|\n'
        'Content-Length: 2|\n'
        'Content-Type: text/plain|\n'
        '|\n'
        '42'
    )
