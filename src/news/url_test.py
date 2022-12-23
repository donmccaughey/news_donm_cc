from .url import URL


def test_eq_and_hash():
    url1 = URL('https://example.com')
    url2 = URL('https://example.com')

    assert url1 == url2
    assert hash(url1) == hash(url2)


def test_str_and_repr():
    url = URL('https://www.example.com/foo/bar?baz#fid')

    assert 'https://www.example.com/foo/bar?baz#fid' == str(url)
    assert "URL('https://www.example.com/foo/bar?baz#fid')" == repr(url)
