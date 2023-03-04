from .url import clean_query, URL


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


def test_clean_query_for_clean():
    assert clean_query('id=123&foo=bar') == 'id=123&foo=bar'


def test_clean_query_for_dirty():
    assert clean_query('utm_source=rss&utm_medium=rss&utm_campaign=foo') == ''


def test_clean_query_for_empty(caplog):
    assert clean_query('') == ''
    assert len(caplog.messages) == 0


def test_url_clean_for_clean_url():
    url = URL('https://example.com').clean()

    assert url == URL('https://example.com')


def test_url_clean_for_clean_url_with_query():
    url = URL('https://example.com?id=123&foo=bar').clean()

    assert url == URL('https://example.com?id=123&foo=bar')


def test_url_clean_for_dirty_url():
    url = URL(
        'https://acoup.blog/2022/12/02/collections-why-roman-egypt-was-such-a-strange-province/?utm_source=rss&utm_medium=rss&utm_campaign=collections-why-roman-egypt-was-such-a-strange-province'
    ).clean()

    assert url == URL('https://acoup.blog/2022/12/02/collections-why-roman-egypt-was-such-a-strange-province/')


def test_url_clean_for_clean_and_dirty_url_params():
    url = URL(
        'https://queue.acm.org/detail.cfm?id=2898444&utm_source=daringfireball&utm_campaign=df2023'
    ).clean()

    assert url == URL('https://queue.acm.org/detail.cfm?id=2898444')


def test_url_clean_for_fragment():
    url = URL('https://example.com#some-anchor').clean()

    assert url == URL('https://example.com')


def test_identity_for_bare_url():
    url = URL('https://fivethirtyeight.com/features/lionel-messi-is-impossible/')

    assert url.identity == 'fivethirtyeight.com'


def test_identity_for_web_url():
    url = URL('https://web.archive.org')

    assert url.identity == 'archive.org'


def test_identity_for_www_url():
    url = URL('https://www.nature.com/articles/srep00487')

    assert url.identity == 'nature.com'

    url = URL('https://www.com')

    assert url.identity == 'www.com'

    url = URL('https://www2.lib.uchicago.edu/keith/emacs/')

    assert url.identity == 'lib.uchicago.edu'


def test_identity_for_blog_url():
    url = URL('https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/')

    assert url.identity == 'lastpass.com'


def test_identity_for_cnn():
    url = URL('https://lite.cnn.com/en/article/h_83938cfff92036cf0e1b55ced9febc77')

    assert url.identity == 'cnn.com'


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

    url = URL('https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca')

    assert url.identity == 'github.com/timvisee'


def test_identity_for_medium():
    url = URL('https://felipepepe.medium.com/before-genshin-impact-a-brief-history-of-chinese-rpgs-bc962fc29908')

    assert url.identity == 'felipepepe.medium.com'

    url = URL('https://medium.com/@ElizAyer/meetings-are-the-work-9e429dde6aa3')

    assert url.identity == 'medium.com/@ElizAyer'


def test_identity_for_microsoft_devblogs():
    url = URL('https://devblogs.microsoft.com/oldnewthing/20221216-00/?p=107598')

    assert url.identity == 'devblogs.microsoft.com/oldnewthing'


def test_identity_for_npr():
    url = URL('https://text.npr.org/1144331954')

    assert url.identity == 'npr.org'


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


def test_identity_for_source_hut():
    url = URL('https://sr.ht/~icefox/oorandom/')

    assert url.identity == 'sr.ht/~icefox'


def test_identity_for_treehouse():
    url = URL('https://social.treehouse.systems/@marcan/109917995005981968')

    assert url.identity == 'social.treehouse.systems/@marcan'


def test_identity_for_twitter():
    url = URL('https://twitter.com/app4soft/status/1606784614793633794')

    assert url.identity == 'twitter.com/app4soft'
