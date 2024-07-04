from datetime import datetime, timezone, timedelta
from serialize import JSONDict

from .item import Item
from .source import Source
from .url import NormalizedURL, URL


def test_eq_and_hash():
    item1 = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=NOW,
        modified=NOW,
    )
    item1_dup = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1 Duplicate',
        [Source(NormalizedURL('https://alt-source.com/1-dup'), 'as')],
        created=NOW,
        modified=NOW,
    )
    item2 = Item(
        NormalizedURL('https://example.com/2'),
        'Item 2',
        [Source(NormalizedURL('https://source.com/2'), 'so')],
        created=NOW,
        modified=NOW,
    )

    assert item1 == item1_dup
    assert hash(item1) == hash(item1_dup)

    assert item1 != item2


def test_str_and_repr():
    item = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=NOW,
        modified=NOW,
    )

    assert str(item) == '"Item 1" (https://example.com/1)'
    assert repr(item) == "Item(NormalizedURL('https://example.com/1'), 'Item 1', [Source(NormalizedURL('https://source.com/1'), 'so', 1)])"


def test_lt_by_sorting():
    item1 = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=THREE_DAYS_AGO,
        modified=NOW,
    )
    item2 = Item(
        NormalizedURL('https://example.com/2'),
        'Item 2',
        [Source(NormalizedURL('https://source.com/2'), 'so')],
        created=TWO_DAYS_AGO,
        modified=NOW,
    )
    item3 = Item(
        NormalizedURL('https://example.com/3'),
        'Item 3',
        [Source(NormalizedURL('https://source.com/3'), 'so')],
        created=YESTERDAY,
        modified=NOW,
    )
    item4 = Item(
        NormalizedURL('https://example.com/4'),
        'Item 4',
        [Source(NormalizedURL('https://source.com/4'), 'so')],
        created=AN_HOUR_AGO,
        modified=NOW,
    )

    sorted_items = sorted([item2, item4, item1, item3])

    assert sorted_items[0].title == 'Item 4'
    assert sorted_items[1].title == 'Item 3'
    assert sorted_items[2].title == 'Item 2'
    assert sorted_items[3].title == 'Item 1'


def test_lt_by_sorting_for_equal_created_sorts_on_url():
    item1 = Item(
        NormalizedURL('https://aaa.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=AN_HOUR_AGO,
        modified=NOW,
    )
    item2 = Item(
        NormalizedURL('https://bbb.com/2'),
        'Item 2',
        [Source(NormalizedURL('https://source.com/2'), 'so')],
        created=AN_HOUR_AGO,
        modified=NOW,
    )
    item3 = Item(
        NormalizedURL('https://ccc.com/3'),
        'Item 3',
        [Source(NormalizedURL('https://source.com/3'), 'so')],
        created=AN_HOUR_AGO,
        modified=NOW,
    )

    sorted_items = sorted([item2, item3, item1])

    assert sorted_items[0].title == 'Item 1'
    assert sorted_items[1].title == 'Item 2'
    assert sorted_items[2].title == 'Item 3'


def test_count():
    item = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so', 2)],
        created=NOW,
        modified=NOW,
    )

    assert item.count == 2

    alt_source = Source(NormalizedURL('https://alt-source.com/2'), 'alt', 1)
    item.sources.append(alt_source)

    assert item.count == 3


def test_different_sources():
    item1 = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=NOW,
        modified=NOW,
    )

    assert len(item1.different_sources) == 1

    item2 = Item(
        NormalizedURL('https://example.com/2'),
        'Item 2',
        [Source(NormalizedURL('https://example.com/2'), 'so')],
        created=NOW,
        modified=NOW,
    )

    assert len(item2.different_sources) == 0


def test_update_from_with_new_source():
    source = Source(NormalizedURL('https://source.com/1'), 'so', 1)
    existing = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [source],
        created=NOW,
        modified=NOW,
    )

    alt_source = Source(NormalizedURL('https://alt-source.com/2'), 'alt', 1)
    other = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [alt_source],
        created=NOW,
        modified=NOW,
    )

    existing.update_from(other)

    assert len(existing.sources) == 2
    assert existing.sources[0] == source
    assert existing.sources[0].count == 1
    assert existing.sources[1] == alt_source
    assert existing.sources[1].count == 1


def test_update_from_with_same_source():
    source = Source(NormalizedURL('https://source.com/1'), 'so', 1)
    existing = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [source],
        created=NOW,
        modified=NOW,
    )

    source_dup = Source(NormalizedURL('https://source.com/1'), 'so', 1)
    other = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [source_dup],
        created=NOW,
        modified=NOW,
    )

    existing.update_from(other)

    assert len(existing.sources) == 1
    assert existing.sources[0] == source
    assert existing.sources[0].count == 2

    assert source_dup.count == 1


def test_decode_from_sources():
    encoded: JSONDict = {
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
        'seq_id': 17,
    }

    item = Item.decode(encoded)

    assert item.url == URL('https://example.com/1')
    assert item.title == 'Item 1'
    assert len(item.sources) == 2
    assert item.sources[0].url == URL('https://source.com/1')
    assert item.sources[0].site_id == 'so'
    assert item.sources[1].url == URL('https://alt-source.com/2')
    assert item.sources[1].site_id == 'alt'
    assert item.seq_id == 17


def test_encode():
    dt = datetime.fromisoformat('2022-12-22T16:36:54.143222+00:00')
    item1 = Item(
        NormalizedURL('https://example.com/1'),
        'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        created=dt,
        modified=dt,
        seq_id=11,
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
    assert encoded['seq_id'] == 11


NOW = datetime.now(timezone.utc)
AN_HOUR_AGO = NOW - timedelta(hours=1)
YESTERDAY = NOW - timedelta(days=1)
TWO_DAYS_AGO = NOW - timedelta(days=2)
THREE_DAYS_AGO = NOW - timedelta(days=3)
