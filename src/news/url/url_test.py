from pytest import mark
from .url import URL


def test_eq_and_hash():
    url1 = URL('https://example.com/1')
    url1_dup = URL('https://example.com/1')
    url2 = URL('https://example.com/2')

    assert url1 == url1_dup
    assert hash(url1) == hash(url1_dup)

    assert url1 != url2


def test_lt_by_sorting():
    url1 = URL('https://aaa.com/1')
    url2 = URL('https://bbb.com/1')
    url3 = URL('https://ccc.com/2')
    url4 = URL('https://ddd.com/2')

    sorted_urls = sorted([url3, url1, url4, url2])

    assert sorted_urls[0] == url1
    assert sorted_urls[1] == url2
    assert sorted_urls[2] == url3
    assert sorted_urls[3] == url4


def test_str_and_repr():
    url = URL('https://www.example.com/foo/bar?baz#fid')

    assert 'https://www.example.com/foo/bar?baz#fid' == str(url)
    assert "URL('https://www.example.com/foo/bar?baz#fid')" == repr(url)


@mark.parametrize('url, normalized', [
    ('https://example.com', 'https://example.com'),
    (
        'https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023',
        'https://queue.acm.org/detail.cfm?id=2898444',
    ),
    (
        'https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again',
        'https://text.npr.org/1165680024',
    ),
])
def test_url_normalize(url, normalized):
    assert URL(url).normalize() == URL(normalized)
