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

    url = NormalizedURL('https://medium.com/@AminYazdanpanah/how-we-built-webrtc-in-php-a-four-month-journey-of-asynchronous-struggles-shared-libraries-and-38fb7c414c1d')
    assert str(url) == 'https://freedium.cfd/https://medium.com/@AminYazdanpanah/how-we-built-webrtc-in-php-a-four-month-journey-of-asynchronous-struggles-shared-libraries-and-38fb7c414c1d'
    assert url.identity == 'medium.com/@AminYazdanpanah'

    url = NormalizedURL('https://freedium.cfd/https://medium.com/@greptime/how-to-supercharge-your-java-project-with-rust-a-practical-guide-to-jni-integration-with-a-86f60e9708b8')
    assert str(url) == 'https://freedium.cfd/https://medium.com/@greptime/how-to-supercharge-your-java-project-with-rust-a-practical-guide-to-jni-integration-with-a-86f60e9708b8'
    assert url.identity == 'medium.com/@greptime'


def test_eq():
    url1 = NormalizedURL('https://example.com/1')
    url1_dup = URL('https://example.com/1')
    url2 = NormalizedURL('https://example.com/2')

    assert url1 == url1_dup
    assert hash(url1) == hash(url1_dup)

    assert url1 != url2
    assert url1_dup != url2
