from .item import Item
from .url import URL


def test_eq_and_hash():
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        URL('https://source.com/1'),
    )
    item1_dup = Item(
        URL('https://example.com/1'),
        'Item 1 Duplicate',
        URL('https://alt-source.com/1-dup'),
    )
    item2 = Item(
        URL('https://example.com/2'),
        'Item 2',
        URL('https://source.com/2'),
    )

    assert item1 == item1_dup
    assert hash(item1) == hash(item1_dup)

    assert item1 != item2


def test_str_and_repr():
    item = Item(
        URL('https://example.com/1'),
        'Item 1',
        URL('https://source.com/1'),
    )

    assert str(item) == '"Item 1" (https://example.com/1)'
    assert repr(item) == "Item(URL('https://example.com/1'), 'Item 1', URL('https://source.com/1'))"
