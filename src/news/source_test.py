from .source import Source
from .url import URL


def test_eq_and_hash():
    source1 = Source(URL('https://source.com/1'), 'so')
    source1_dup = Source(URL('https://source.com/1'), 'so')
    source2 = Source(URL('https://source.com/2'), 'so')
    alt_source = Source(URL('https://alt-source.com/1'), 'as')

    assert source1 == source1_dup
    assert hash(source1) == hash(source1_dup)

    assert source1 != source2
    assert source1 != alt_source


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


def test_decode():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
    })

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'so'


def test_encode():
    source = Source(URL('https://source.com/1'), 'so')

    assert source.encode() == {
        'url': 'https://source.com/1',
        'site_id': 'so',
    }
