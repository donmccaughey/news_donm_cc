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


CLEAN_QUERY_TESTS = [
    ('', ''),
    ('id=123&foo=bar', 'id=123&foo=bar'),
    ('blank=', 'blank='),
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
]


@mark.parametrize('url, cleaned', URL_CLEAN_TESTS)
def test_url_clean(url, cleaned):
    assert URL(url).clean() == URL(cleaned)


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
    ('lrb.co.uk', 'https://www.lrb.co.uk/the-paper/v45/n11/neal-ascherson/kings-grew-pale'),

    # `www` is removed
    ('nature.com', 'https://www.nature.com/articles/srep00487'),

    # `www2` domain is removed
    ('lib.uchicago.edu', 'https://www2.lib.uchicago.edu/keith/emacs'),


    # -- `/<user>/<...>` paths

    ('gitlab.com/cznic', 'https://gitlab.com/cznic/sqlite'),
    ('sites.google.com/site/misterzeropage', 'https://sites.google.com/site/misterzeropage/'),
    ('people.kernel.org/monsieuricon', 'https://people.kernel.org/monsieuricon/fix-your-mutt'),
    ('kickstarter.com/projects/robwalling', 'https://www.kickstarter.com/projects/robwalling/the-saas-playbook-by-rob-walling'),
    ('devblogs.microsoft.com/oldnewthing', 'https://devblogs.microsoft.com/oldnewthing/20221216-00/?p=107598'),
    ('twitter.com/app4soft', 'https://twitter.com/app4soft/status/1606784614793633794'),


    # == `/~<user>/<...>` paths

    ('sr.ht/~icefox', 'https://sr.ht/~icefox/oorandom/'),
    ('git.sr.ht/~akkartik', 'https://git.sr.ht/~akkartik/snap.love'),


    # -- `/@<user>/<...>` paths

    ('flipboard.social/@mike', 'https://flipboard.social/@mike/110137461654913391'),
    ('floss.social/@ademalsasa', 'https://floss.social/@ademalsasa/109597861116785251'),
    ('mastodon.social/@mastodonusercount', 'https://mastodon.social/@mastodonusercount/110051957865629817'),
    ('social.network.europa.eu/@EU_Commission', 'https://social.network.europa.eu/@EU_Commission/110140022257601348'),
    ('social.treehouse.systems/@marcan', 'https://social.treehouse.systems/@marcan/109917995005981968'),
    ('mastodon.nl/@vickyvdtogt', 'https://mastodon.nl/@vickyvdtogt/110196805189572082'),
    ('masto.ai/@mg', 'https://masto.ai/@mg/110212843144499061'),


    # -- package repositories

    ('crates.io/crates/fundsp', 'https://crates.io/crates/fundsp/0.13.0'),
    ('npmjs.com/package/express', 'https://www.npmjs.com/package/express'),
    ('pypi.org/project/pytest', 'https://pypi.org/project/pytest/'),


    # -- github

    ('github.com', 'https://github.com'),
    ('github.com/electronicarts', 'https://github.com/electronicarts/EAStdC/blob/master/include/EAStdC/EABitTricks.h'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI'),
    ('github.com/Immediate-Mode-UI', 'https://github.com/Immediate-Mode-UI/Nuklear'),
    ('github.com/microsoft', 'https://github.com/microsoft/WSA/discussions/167'),
    ('github.com/readme', 'https://github.com/readme/featured/nuclear-fusion-open-source'),
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


URL_REWRITE_TESTS = [
    (
        'https://languagelearningwithnetflix.com/',
        'https://languagelearningwithnetflix.com/'
    ),
    (
        'https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/',
        'https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'
    ),

    # NPR, no section
    (
        'https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again',
        'https://text.npr.org/1165680024',
    ),
    # NPR, sections
    (
        'https://www.npr.org/sections/money/2023/05/02/1172791281/this-company-adopted-ai-heres-what-happened-to-its-human-workers',
        'https://text.npr.org/1172791281',
    ),
]


@mark.parametrize('url, rewritten', URL_REWRITE_TESTS)
def test_url_rewrite(url, rewritten):
    assert URL(url).rewrite() == URL(rewritten)
