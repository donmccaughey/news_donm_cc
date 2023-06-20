from .source import Source
from .url import URL


def test_eq_and_hash():
    source1 = Source(URL('https://source.com/1'), 'so', 2)
    source1_dup = Source(URL('https://source.com/1'), 'so', 1)
    source2 = Source(URL('https://source.com/2'), 'so')
    alt_source = Source(URL('https://alt-source.com/1'), 'as', 3)

    assert source1 == source1_dup
    assert hash(source1) == hash(source1_dup)

    assert source1 != source2
    assert source1 != alt_source


def test_lt_by_sorting():
    source1 = Source(URL('https://source.com/1'), 'aa', 2)
    source2 = Source(URL('https://example.com/1'), 'bb', 1)
    source3 = Source(URL('https://alt-example.com/2'), 'cc')
    source4 = Source(URL('https://alt-source.com/1'), 'dd', 3)

    sorted_sources = sorted([source3, source1, source4, source2])

    assert sorted_sources[0].site_id == 'aa'
    assert sorted_sources[1].site_id == 'bb'
    assert sorted_sources[2].site_id == 'cc'
    assert sorted_sources[3].site_id == 'dd'


def test_source_cleans_url():
    source = Source(
        URL('https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023'),
        'so',
    )

    assert source.url == URL('https://queue.acm.org/detail.cfm?id=2898444')


def test_source_rewrites_url():
    source = Source(
        URL('https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'),
        'so',
    )

    assert source.url == URL('https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/')


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
    source = Source(URL('https://source.com/1'), 'so', 3)

    assert source.encode() == {
        'url': 'https://source.com/1',
        'site_id': 'so',
        'count': 3,
    }
