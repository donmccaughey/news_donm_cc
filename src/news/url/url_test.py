from pytest import mark
from .url import clean_query, clean_url, URL


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


CLEAN_QUERY_TESTS = [
    ('', ''),
    ('id=123&foo=bar', 'id=123&foo=bar'),
    ('blank=', 'blank='),
    ('leadSource=uverify%20wall', ''),
    ('TupleSpace', 'TupleSpace'),
    ('utm_source=rss&utm_medium=rss&utm_campaign=foo', ''),
]


@mark.parametrize('query, cleaned', CLEAN_QUERY_TESTS)
def test_clean_query(query, cleaned, caplog):
    assert clean_query(query) == cleaned
    assert len(caplog.messages) == 0


URL_CLEAN_TESTS = [
    ('https://example.com', 'https://example.com'),
    ('https://example.com?id=123&foo=bar', 'https://example.com?id=123&foo=bar'),
    (
        'https://acoup.blog/2022/12/02/collections-why-roman-egypt-was-such-a-strange-province/?utm_source=rss&utm_medium=rss&utm_campaign=collections-why-roman-egypt-was-such-a-strange-province',
        'https://acoup.blog/2022/12/02/collections-why-roman-egypt-was-such-a-strange-province/',
    ),
    (
        'https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023',
        'https://queue.acm.org/detail.cfm?id=2898444',
    ),
    (
        'https://www.nytimes.com/live/2023/05/24/us/desantis-2024-election-president/ron-desantis-2024-presidential-election?smid=url-share',
        'https://www.nytimes.com/live/2023/05/24/us/desantis-2024-election-president/ron-desantis-2024-presidential-election',
    ),
    ('https://example.com#some-anchor', 'https://example.com'),
    (
        'https://www.bloomberg.com/news/articles/2023-06-15/alphabet-selling-google-domains-assets-to-squarespace?leadSource=uverify%20wall',
        'https://www.bloomberg.com/news/articles/2023-06-15/alphabet-selling-google-domains-assets-to-squarespace',
    ),
    (
        'https://www.bloomberg.com/opinion/articles/2023-06-27/silicon-valley-is-on-drugs#xj4y7vzkg',
        'https://www.bloomberg.com/opinion/articles/2023-06-27/silicon-valley-is-on-drugs',
    ),
]


@mark.parametrize('url, cleaned', URL_CLEAN_TESTS)
def test_clean_url(url, cleaned):
    assert clean_url(url) == cleaned


URL_NORMALIZE_TESTS = [
    ('https://example.com', 'https://example.com'),
    (
        'https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023',
        'https://queue.acm.org/detail.cfm?id=2898444',
    ),
    (
        'https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again',
        'https://text.npr.org/1165680024',
    ),
]


@mark.parametrize('url, normalized', URL_NORMALIZE_TESTS)
def test_url_normalize(url, normalized):
    assert URL(url).normalize() == URL(normalized)
