from pytest import mark
from urllib.parse import urlsplit
from .rewrite import rewrite_reuters_url, rewrite_twitter_url, rewrite_url, rewrite_npr_url, rewrite_reddit_url


@mark.parametrize('url, rewritten', [
    (
        'https://languagelearningwithnetflix.com/',
        'https://languagelearningwithnetflix.com/'
    ),
    (
        'https://www.reuters.com/legal/transactional/venmo-cash-app-users-sue-apple-over-peer-to-peer-payment-fees-2023-11-20/',
        'https://neuters.de/legal/transactional/venmo-cash-app-users-sue-apple-over-peer-to-peer-payment-fees-2023-11-20/',
    ),
    (
        'https://twitter.com/eshear/status/1726526112019382275?s=46&t=a8Pjw_2Gzth_zpOPBTHQaw',
        'https://nitter.net/eshear/status/1726526112019382275',
    ),

    # Reddit variations
    (
        'https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/',
        'https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'
    ),
    (
            'https://sh.reddit.com/r/uBlockOrigin/comments/17wu2gz/google_confirms_they_will_disable_ublock_origin/',
            'https://old.reddit.com/r/uBlockOrigin/comments/17wu2gz/google_confirms_they_will_disable_ublock_origin/',
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
])
def test_rewrite_url(url, rewritten):
    assert rewrite_url(url) == rewritten


@mark.parametrize('url, rewritten', [
    # no section
    (
        'https://www.npr.org/2023/03/23/1165680024/perennial-rice-plant-once-harvest-again-and-again',
        'https://text.npr.org/1165680024',
    ),
    # sections
    (
        'https://www.npr.org/sections/money/2023/05/02/1172791281/this-company-adopted-ai-heres-what-happened-to-its-human-workers',
        'https://text.npr.org/1172791281',
    ),
    # not a news story
    (
        'https://www.npr.org/newsletter/news',
        None,
    )
])
def test_rewrite_npr_url(url, rewritten):
    scheme, netloc, path, query, fragment = urlsplit(url)
    assert rewrite_npr_url(scheme, path) == rewritten


@mark.parametrize('url, rewritten', [
    (
        'https://www.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/',
        'https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/',
    ),
    (
        'https://sh.reddit.com/r/uBlockOrigin/comments/17wu2gz/google_confirms_they_will_disable_ublock_origin/',
        'https://old.reddit.com/r/uBlockOrigin/comments/17wu2gz/google_confirms_they_will_disable_ublock_origin/',
    ),
])
def test_rewrite_reddit_url(url, rewritten):
    scheme, netloc, path, query, fragment = urlsplit(url)
    assert rewrite_reddit_url(scheme, path, query, fragment) == rewritten


@mark.parametrize('url, rewritten', [
    (
            'https://www.reuters.com/legal/transactional/venmo-cash-app-users-sue-apple-over-peer-to-peer-payment-fees-2023-11-20/',
            'https://neuters.de/legal/transactional/venmo-cash-app-users-sue-apple-over-peer-to-peer-payment-fees-2023-11-20/',
    ),
])
def test_rewrite_reuters_url(url, rewritten):
    scheme, netloc, path, query, fragment = urlsplit(url)
    assert rewrite_reuters_url(scheme, path) == rewritten


@mark.parametrize('url, rewritten', [
    (
        'https://twitter.com/eastdakota/status/1726735785188073726',
        'https://nitter.net/eastdakota/status/1726735785188073726',
    ),
    (
        'https://twitter.com/eshear/status/1726526112019382275?s=46&t=a8Pjw_2Gzth_zpOPBTHQaw',
        'https://nitter.net/eshear/status/1726526112019382275',
    )
])
def test_rewrite_twitter_url(url, rewritten):
    scheme, netloc, path, query, fragment = urlsplit(url)
    assert rewrite_twitter_url(scheme, path) == rewritten
