from datetime import datetime, timezone, timedelta

from .item import Item
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
    assert repr(item) == "Item(URL('https://example.com/1'), 'Item 1', [Source(URL('https://source.com/1'), 'so', 1)])"


def test_lt_by_sorting():
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
        created=THREE_DAYS_AGO,
    )
    item2 = Item(
        URL('https://example.com/2'),
        'Item 2',
        [Source(URL('https://source.com/2'), 'so')],
        created=TWO_DAYS_AGO,
    )
    item3 = Item(
        URL('https://example.com/3'),
        'Item 3',
        [Source(URL('https://source.com/3'), 'so')],
        created=YESTERDAY,
    )
    item4 = Item(
        URL('https://example.com/4'),
        'Item 4',
        [Source(URL('https://source.com/4'), 'so')],
        created=AN_HOUR_AGO,
    )

    sorted_items = sorted([item2, item4, item1, item3])

    assert sorted_items[0].title == 'Item 4'
    assert sorted_items[1].title == 'Item 3'
    assert sorted_items[2].title == 'Item 2'
    assert sorted_items[3].title == 'Item 1'


def test_lt_by_sorting_for_equal_created_sorts_on_url():
    item1 = Item(
        URL('https://aaa.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
        created=AN_HOUR_AGO,
    )
    item2 = Item(
        URL('https://bbb.com/2'),
        'Item 2',
        [Source(URL('https://source.com/2'), 'so')],
        created=AN_HOUR_AGO,
    )
    item3 = Item(
        URL('https://ccc.com/3'),
        'Item 3',
        [Source(URL('https://source.com/3'), 'so')],
        created=AN_HOUR_AGO,
    )

    sorted_items = sorted([item2, item3, item1])

    assert sorted_items[0].title == 'Item 1'
    assert sorted_items[1].title == 'Item 2'
    assert sorted_items[2].title == 'Item 3'


def test_count():
    item = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so', 2)],
    )

    assert item.count == 2

    alt_source = Source(URL('https://alt-source.com/2'), 'alt', 1)
    item.sources.append(alt_source)

    assert item.count == 3


def test_different_sources():
    item1 = Item(
        URL('https://example.com/1'),
        'Item 1',
        [Source(URL('https://source.com/1'), 'so')],
    )

    assert len(item1.different_sources) == 1

    item2 = Item(
        URL('https://example.com/2'),
        'Item 2',
        [Source(URL('https://example.com/2'), 'so')],
    )

    assert len(item2.different_sources) == 0


def test_update_from_with_new_source():
    source = Source(URL('https://source.com/1'), 'so', 1)
    existing = Item(
        URL('https://example.com/1'),
        'Item 1',
        [source],
    )

    alt_source = Source(URL('https://alt-source.com/2'), 'alt', 1)
    other = Item(
        URL('https://example.com/1'),
        'Item 1',
        [alt_source],
    )

    existing.update_from(other)

    assert len(existing.sources) == 2
    assert existing.sources[0] == source
    assert existing.sources[0].count == 1
    assert existing.sources[1] == alt_source
    assert existing.sources[1].count == 1


def test_update_from_with_same_source():
    source = Source(URL('https://source.com/1'), 'so', 1)
    existing = Item(
        URL('https://example.com/1'),
        'Item 1',
        [source],
    )

    source_dup = Source(URL('https://source.com/1'), 'so', 1)
    other = Item(
        URL('https://example.com/1'),
        'Item 1',
        [source_dup],
    )

    existing.update_from(other)

    assert len(existing.sources) == 1
    assert existing.sources[0] == source
    assert existing.sources[0].count == 2

    assert source_dup.count == 1


def test_decode_from_source():
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


def test_decode_from_sources():
    encoded = {
        'url': 'https://example.com/1',
        'title': 'Item 1',
        'sources': [
            {
                'url': 'https://source.com/1',
                'site_id': 'so',
            },
            {
                'url': 'https://alt-source.com/2',
                'site_id': 'alt',
            },
        ],
        'created': '2022-12-22T16:36:54.143222+00:00',
        'modified': '2022-12-22T16:36:54.143222+00:00',
    }

    item = Item.decode(encoded)

    assert item.url == URL('https://example.com/1')
    assert item.title == 'Item 1'
    assert len(item.sources) == 2
    assert item.sources[0].url == URL('https://source.com/1')
    assert item.sources[0].site_id == 'so'
    assert item.sources[1].url == URL('https://alt-source.com/2')
    assert item.sources[1].site_id == 'alt'


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
            'count': 1,
        }
    ]
    assert encoded['created'] == '2022-12-22T16:36:54.143222+00:00'
    assert encoded['modified'] == '2022-12-22T16:36:54.143222+00:00'


NOW = datetime.now(timezone.utc)
AN_HOUR_AGO = NOW - timedelta(hours=1)
YESTERDAY = NOW - timedelta(days=1)
TWO_DAYS_AGO = NOW - timedelta(days=2)
THREE_DAYS_AGO = NOW - timedelta(days=3)
