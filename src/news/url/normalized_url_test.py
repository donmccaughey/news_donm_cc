from news.url import NormalizedURL, URL


def test_str_and_repr():
    url = NormalizedURL('https://www.example.com/foo/bar?baz#fid')

    assert 'https://www.example.com/foo/bar?baz' == str(url)
    assert "NormalizedURL('https://www.example.com/foo/bar?baz')" == repr(url)


def test_init():
    url = NormalizedURL('https://example.com')
    assert str(url) == 'https://example.com'
    assert url.identity == 'example.com'

    url = NormalizedURL('https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023')
    assert str(url) == 'https://queue.acm.org/detail.cfm?id=2898444'
    assert url.identity == 'queue.acm.org'

    url = NormalizedURL('https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again')
    assert str(url) == 'https://text.npr.org/1165680024'
    assert url.identity == 'npr.org'


def test_eq():
    url1 = NormalizedURL('https://example.com/1')
    url1_dup = URL('https://example.com/1')
    url2 = NormalizedURL('https://example.com/2')

    assert url1 == url1_dup
    assert hash(url1) == hash(url1_dup)

    assert url1 != url2
    assert url1_dup != url2
