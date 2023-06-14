from datetime import datetime

from .item import Age, Item
from .source import Source
from .url import URL


def test_item_cleans_url():
    item = Item(
        URL('https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )

    assert item.url == URL('https://queue.acm.org/detail.cfm?id=2898444')


def test_item_rewrites_url():
    item = Item(
        URL('https://www.npr.org/sections/money/2023/05/02/1172791281/this-company-adopted-ai-heres-what-happened-to-its-human-workers'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )

    assert item.url == URL('https://text.npr.org/1172791281')


def test_item_rewrites_source_url():
    item = Item(
        URL('https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'),
        'Item 1',
        [Source(URL('https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'), 'so')],
    )

    assert item.sources[0].url == URL('https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/')


def test_eq_and_hash():
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )
    item1_dup = Item(
        URL('https://example.com/1'),
        'Item 1 Duplicate',
        [Source(URL('https://alt-source.com/1-dup'), 'as')],
    )
    item2 = Item(
        URL('https://example.com/2'),
        'Item 2',
        [Source(URL('https://source.com/2'), 'so')],
    )

    assert item1 == item1_dup
    assert hash(item1) == hash(item1_dup)

    assert item1 != item2


def test_str_and_repr():
    item = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )

    assert str(item) == '"Item 1" (https://example.com/1)'
    assert repr(item) == "Item(URL('https://example.com/1'), 'Item 1', [Source(URL('https://source.com/1'), 'so')])"


def test_show_source():
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )

    assert item1.show_source

    item2 = Item(
        URL('https://example.com/2'),
        'Item 2',
        [Source(URL('https://example.com/2'), 'so')],
    )

    assert not item2.show_source


def test_decode_from_source_str():
    encoded = {
        'url': 'https://example.com/1',
        'title': 'Item 1',
        'source': 'https://source.com/1',
        'created': '2022-12-22T16:36:54.143222+00:00',
        'modified': '2022-12-22T16:36:54.143222+00:00',
    }

    item = Item.decode(encoded)

    assert item.url == URL('https://example.com/1')
    assert item.title == 'Item 1'
    assert item.sources[0].url == URL('https://source.com/1')
    assert item.sources[0].site_id == 'hn'
    assert item.age == Age.UNKNOWN


def test_decode_from_source_dict():
    encoded = {
        'url': 'https://example.com/1',
        'title': 'Item 1',
        'source': {
            'url': 'https://source.com/1',
            'site_id': 'so',
        },
        'created': '2022-12-22T16:36:54.143222+00:00',
        'modified': '2022-12-22T16:36:54.143222+00:00',
    }

    item = Item.decode(encoded)

    assert item.url == URL('https://example.com/1')
    assert item.title == 'Item 1'
    assert item.sources[0].url == URL('https://source.com/1')
    assert item.sources[0].site_id == 'so'
    assert item.age == Age.UNKNOWN


def test_encode():
    dt = datetime.fromisoformat('2022-12-22T16:36:54.143222+00:00')
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
        created=dt,
        modified=dt,
    )

    encoded = item1.encode()

    assert encoded['url'] == 'https://example.com/1'
    assert encoded['title'] == 'Item 1'
    assert encoded['sources'] == [
        {
            'url': 'https://source.com/1',
            'site_id': 'so',
        }
    ]
    assert encoded['created'] == '2022-12-22T16:36:54.143222+00:00'
    assert encoded['modified'] == '2022-12-22T16:36:54.143222+00:00'
