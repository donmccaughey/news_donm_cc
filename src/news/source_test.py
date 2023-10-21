from .source import Source
from .url import NormalizedURL, URL


def test_eq_and_hash():
    source1 = Source(NormalizedURL('https://source.com/1'), 'so', 2)
    source1_dup = Source(NormalizedURL('https://source.com/1'), 'so', 1)
    source2 = Source(NormalizedURL('https://source.com/2'), 'so')
    alt_source = Source(NormalizedURL('https://alt-source.com/1'), 'as', 3)

    assert source1 == source1_dup
    assert hash(source1) == hash(source1_dup)

    assert source1 != source2
    assert source1 != alt_source


def test_lt_by_sorting():
    source1 = Source(NormalizedURL('https://source.com/1'), 'aa', 2)
    source2 = Source(NormalizedURL('https://example.com/1'), 'bb', 1)
    source3 = Source(NormalizedURL('https://alt-example.com/2'), 'cc')
    source4 = Source(NormalizedURL('https://alt-source.com/1'), 'dd', 3)

    sorted_sources = sorted([source3, source1, source4, source2])

    assert sorted_sources[0].site_id == 'aa'
    assert sorted_sources[1].site_id == 'bb'
    assert sorted_sources[2].site_id == 'cc'
    assert sorted_sources[3].site_id == 'dd'


def test_update_from():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
        'count': 2,
    })
    source_dup = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
        'count': 1,
    })

    source.update_from(source_dup)

    assert source.count == 3


def test_decode():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
        'count': 2,
    })

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'so'
    assert source.count == 2


def test_decode_missing_count():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
    })

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'so'
    assert source.count == 1


def test_encode():
    source = Source(NormalizedURL('https://source.com/1'), 'so', 3)

    assert source.encode() == {
        'url': 'https://source.com/1',
        'site_id': 'so',
        'count': 3,
    }
