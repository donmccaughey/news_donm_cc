from datetime import datetime, timezone

import pytest
from feedparser import FeedParserDict, parse
from pytest import mark

from .hacker_news import HackerNews


def test_parse_entry_decodes_html_entities():
    d = build_hn_feed(
        title='&amp;lt;3 Deno',
        link='https://matklad.github.io/2023/02/12/a-love-letter-to-deno.html',
        comments='https://news.ycombinator.com/item?id=34767795',
    )
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == '<3 Deno'


def test_parse_entry_decodes_hex_char_entities():
    d = build_hn_feed(
        title='NameCheap&amp;#x27;s email hacked to send Metamask, DHL phishing emails',
        link='https://www.bleepingcomputer.com/news/security/namecheaps-email-hacked-to-send-metamask-dhl-phishing-emails/',
        comments='https://news.ycombinator.com/item?id=34768550',
    )
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == "NameCheap's email hacked to send Metamask, DHL phishing emails"


def test_keep_item_keeps_typical_entry():
    d = build_hn_feed(
        title='Can Doom Run It? An Adding Machine in Doom',
        link='https://blog.otterstack.com/posts/202212-doom-calculator/',
        comments='https://news.ycombinator.com/item?id=34102419',
    )
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))

    assert hn.keep_item(item)


REJECT_SITE_TESTS = [
    pytest.param(
        'If Parrots Can Talk, Why Can’t Monkeys?',
        'https://english.elpais.com/science-tech/2023-01-10/if-parrots-can-talk-why-cant-monkeys.html',
        'https://news.ycombinator.com/item?id=35431466',
        id='english.elpais.com',
    ),
    pytest.param(
        'San Francisco is getting cold feet about self-driving car tests',
        'https://www.newscientist.com/article/2356888-san-francisco-is-getting-cold-feet-about-self-driving-car-tests/',
        'https://news.ycombinator.com/item?id=34608179',
        id='newscientist.com',
    ),
    pytest.param(
        'Why to start a startup in a bad economy (2008)',
        'http://paulgraham.com/badeconomy.html',
        'https://news.ycombinator.com/item?id=34429869',
        id='paulgraham.com',
    ),
    pytest.param(
        'Travelling Just for the People',
        'https://sive.rs/travp',
        'https://news.ycombinator.com/item?id=34733694',
        id='sive.rs',
    ),
    pytest.param(
        'Highlights from the Comments on IRBs',
        'https://astralcodexten.substack.com/p/highlights-from-the-comments-on-irbs',
        'https://news.ycombinator.com/item?id=35608036',
        id='astralcodexten.substack.com',
    ),
    pytest.param(
        '“Luxury” construction causes high rents like umbrellas cause rain',
        'https://noahpinion.substack.com/p/luxury-construction-causes-high-rents',
        'https://news.ycombinator.com/item?id=35668072',
        id='noahpinion.substack.com',
    ),
    pytest.param(
        'Philosophy’s No-Go Zone',
        'https://quillette.com/2023/04/17/philosophys-no-go-zone/',
        'https://news.ycombinator.com/item?id=35678299',
        id='quillette.com',
    ),
    pytest.param(
        'Borrowers with High Credit Scores Penalized Under New Federal Mortgage Fee Plan',
        'https://reason.com/2023/04/21/borrowers-with-high-credit-scores-penalized-under-new-federal-mortgage-fee-plan/',
        'https://news.ycombinator.com/item?id=35676765',
        id='reason.com',
    ),
    pytest.param(
        'Someone Has to Run the Fabs',
        'https://www.noahpinion.blog/p/repost-someone-has-to-run-the-fabs',
        'https://news.ycombinator.com/item?id=35715679',
        id='noahpinion.blog',
    ),
    pytest.param(
        'Brave Search removes last remnant of Bing from search results page',
        'https://brave.com/search-independence/',
        'https://news.ycombinator.com/item?id=35730711',
        id='brave.com',
    ),
]


@mark.parametrize('title, link, comments', REJECT_SITE_TESTS)
def test_keep_item_rejects_site(title, link, comments):
    d = build_hn_feed(str(title), str(link), str(comments))
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))

    assert not hn.keep_item(item)


def test_is_entry_valid_rejects():
    hn = HackerNews()
    entry = {}

    assert not hn.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff'}

    assert not hn.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff', 'title': 'Stuff'}

    assert not hn.is_entry_valid(entry)

    entry = {
        'comments': 'https://example.com/comments',
        'link': 'https://example.com/stuff',
        'title': 'Stuff'
    }

    assert hn.is_entry_valid(entry)


def build_hn_feed(title: str, link: str, comments: str) -> FeedParserDict:
    feed = [
        '<rss version="2.0">',
        '<channel>',
        '<item>',
    ]
    if title:
        feed.append(f'<title>{title}</title>')
    if link:
        feed.append(f'<link>{link}</link>')
    if comments:
        feed.append(f'<comments>{comments}</comments>')
    feed += [
        '</item>',
        '</channel>',
        '</rss>',
    ]
    return parse('\n'.join(feed))
