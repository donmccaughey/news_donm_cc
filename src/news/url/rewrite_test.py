from pytest import mark
from urllib.parse import urlsplit
from .rewrite import rewrite_url, rewrite_npr_url, rewrite_reddit_url


@mark.parametrize('url, rewritten', [
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
        'https://old.reddit.com/r/pics/comments/13a00ge/a_canadian_goose_that_comes_back_year_after_year/'
    ),
])
def test_rewrite_reddit_url(url, rewritten):
    scheme, netloc, path, query, fragment = urlsplit(url)
    assert rewrite_reddit_url(scheme, path, query, fragment) == rewritten
