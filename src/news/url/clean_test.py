from pytest import mark
from .clean import clean_query, clean_url


@mark.parametrize('query, cleaned', [
    ('', ''),
    ('id=123&foo=bar', 'id=123&foo=bar'),
    ('blank=', 'blank='),
    ('leadSource=uverify%20wall', ''),
    ('TupleSpace', 'TupleSpace'),
    ('utm_source=rss&utm_medium=rss&utm_campaign=foo', ''),
])
def test_clean_query(query, cleaned, caplog):
    assert clean_query(query) == cleaned
    assert len(caplog.messages) == 0


@mark.parametrize('url, cleaned', [
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
])
def test_clean_url(url, cleaned):
    assert clean_url(url) == cleaned
