from .source import Source
from .url import URL


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


def test_decode_from_str():
    source = Source.decode('https://source.com/1')

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'hn'


def test_decode_from_dict():
    source = Source.decode({
        'url': 'https://source.com/1',
        'site_id': 'so',
    })

    assert source.url == URL('https://source.com/1')
    assert source.site_id == 'so'
