from .url import URL


def test_eq_and_hash():
    url1 = URL('https://example.com/1')
    url1_dup = URL('https://example.com/1')
    url2 = URL('https://example.com/2')

    assert url1 == url1_dup
    assert hash(url1) == hash(url1_dup)

    assert url1 != url2


def test_str_and_repr():
    url = URL('https://www.example.com/foo/bar?baz#fid')

    assert 'https://www.example.com/foo/bar?baz#fid' == str(url)
    assert "URL('https://www.example.com/foo/bar?baz#fid')" == repr(url)


def test_identity_for_bare_url():
    url = URL('https://fivethirtyeight.com/features/lionel-messi-is-impossible/')

    assert url.identity == 'fivethirtyeight.com'


def test_identity_for_www_url():
    url = URL('https://www.nature.com/articles/srep00487')

    assert url.identity == 'nature.com'

    url = URL('https://www.com')

    assert url.identity == 'www.com'


def test_identity_for_blog_url():
    url = URL('https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/')

    assert url.identity == 'lastpass.com'


def test_identity_for_github():
    url = URL('https://github.com/electronicarts/EAStdC/blob/master/include/EAStdC/EABitTricks.h')

    assert url.identity == 'github.com/electronicarts'

    url = URL('https://github.com/microsoft/WSA/discussions/167')

    assert url.identity == 'github.com/microsoft'

    url = URL('https://github.com/Immediate-Mode-UI/Nuklear')

    assert url.identity == 'github.com/Immediate-Mode-UI'

    url = URL('https://github.com/Immediate-Mode-UI')

    assert url.identity == 'github.com/Immediate-Mode-UI'

    url = URL('https://github.com')

    assert url.identity == 'github.com'


def test_identity_for_reddit():
    url = URL('https://www.reddit.com/r/printSF/comments/zuit3f/best_place_to_start_reading_isaac_asimov/')

    assert url.identity == 'reddit.com/r/printSF'

    url = URL('https://www.reddit.com/r/printSF')

    assert url.identity == 'reddit.com/r/printSF'

    url = URL('https://www.reddit.com/wiki/reddiquette/')

    assert url.identity == 'reddit.com'

    url = URL('https://www.reddit.com/rules/')

    assert url.identity == 'reddit.com'

    url = URL('https://www.reddit.com')

    assert url.identity == 'reddit.com'


def test_identity_for_old_reddit():
    url = URL('https://old.reddit.com/r/YouShouldKnow/comments/zl8ko3/ysk_apple_music_deletes_your_original_songs_and/')

    assert url.identity == 'reddit.com/r/YouShouldKnow'


def test_identity_for_twitter():
    url = URL('https://twitter.com/app4soft/status/1606784614793633794')

    assert url.identity == 'twitter.com/app4soft'
