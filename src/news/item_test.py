from .item import Item
from .url import URL


def test_str_and_repr():
    item = Item(
        URL('https://example.com/1'),
        'Item 1',
        URL('https://source.com/1'),
    )

    assert str(item) == '"Item 1" (https://example.com/1)'
    assert repr(item) == "Item(URL('https://example.com/1'), 'Item 1', URL('https://source.com/1'))"
