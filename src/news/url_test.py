from pytest import mark
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


IDENTITY_TESTS = [
    # bare domain is untouched
    ('fivethirtyeight.com', 'https://fivethirtyeight.com/features/lionel-messi-is-impossible/'),

    # less than three domain parts is unchanged
    ('www.com', 'https://www.com'),


    # -- standard top level domains are removed

    # `blog` is removed
    ('lastpass.com', 'https://blog.lastpass.com/2022/12/notice-of-recent-security-incident/'),

    # `web` is removed
    ('archive.org', 'https://web.archive.org'),

    # `www` is removed
    ('nature.com', 'https://www.nature.com/articles/srep00487'),

    # `www2` domain is removed
    ('lib.uchicago.edu', 'https://www2.lib.uchicago.edu/keith/emacs'),


    # -- `/<user>/<...>` paths

    ('gitlab.com/cznic', 'https://gitlab.com/cznic/sqlite'),
    ('devblogs.microsoft.com/oldnewthing', 'https://devblogs.microsoft.com/oldnewthing/20221216-00/?p=107598'),
    ('sr.ht/~icefox', 'https://sr.ht/~icefox/oorandom/'),
    ('twitter.com/app4soft', 'https://twitter.com/app4soft/status/1606784614793633794'),

    # -- `/@<user>/<...>` paths

    ('social.network.europa.eu/@EU_Commission', 'https://social.network.europa.eu/@EU_Commission/110140022257601348'),
    ('flipboard.social/@mike', 'https://flipboard.social/@mike/110137461654913391'),
    ('social.treehouse.systems/@marcan', 'https://social.treehouse.systems/@marcan/109917995005981968'),


    # -- github
    ('github.com', 'https://github.com'),
    ('github.com/electronicarts', 'https://github.com/electronicarts/EAStdC/blob/master/include/EAStdC/EABitTricks.h'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI/Nuklear'),
    ('github.com/microsoft', 'https://github.com/microsoft/WSA/discussions/167'),
    ('github.com/timvisee', 'https://gist.github.com/timvisee/fcda9bbdff88d45cc9061606b4b923ca'),


    # -- medium

    ('felipepepe.medium.com', 'https://felipepepe.medium.com/before-genshin-impact-a-brief-history-of-chinese-rpgs-bc962fc29908'),
    ('medium.com/@ElizAyer', 'https://medium.com/@ElizAyer/meetings-are-the-work-9e429dde6aa3'),


    # -- reddit

    ('reddit.com/r/printSF', 'https://www.reddit.com/r/printSF'),
    ('reddit.com/r/printSF', 'https://www.reddit.com/r/printSF/comments/zuit3f/best_place_to_start_reading_isaac_asimov/'),
    ('reddit.com', 'https://www.reddit.com'),
    ('reddit.com', 'https://www.reddit.com/rules/'),
    ('reddit.com', 'https://www.reddit.com/wiki/reddiquette/'),

    # `old.reddit.com`
    ('reddit.com/r/YouShouldKnow', 'https://old.reddit.com/r/YouShouldKnow/comments/zl8ko3/ysk_apple_music_deletes_your_original_songs_and/'),


    # -- special cases

    # `lite.cnn.com`
    ('cnn.com', 'https://lite.cnn.com/en/article/h_83938cfff92036cf0e1b55ced9febc77'),

    # `text.npr.org'
    ('npr.org', 'https://text.npr.org/1144331954'),
]


@mark.parametrize('identity, url', IDENTITY_TESTS)
def test_identity(identity, url):
    assert URL(url).identity == identity
