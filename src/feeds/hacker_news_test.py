from datetime import datetime, timezone
from feedparser import FeedParserDict, parse

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


def test_keep_entry_keeps_typical_entry():
    d = build_hn_feed(
        title='Can Doom Run It? An Adding Machine in Doom',
        link='https://blog.otterstack.com/posts/202212-doom-calculator/',
        comments='https://news.ycombinator.com/item?id=34102419',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert hn.keep_entry(entry)


def test_keep_entry_rejects_elpais():
    d = build_hn_feed(
        title='If Parrots Can Talk, Why Can’t Monkeys?',
        link='https://english.elpais.com/science-tech/2023-01-10/if-parrots-can-talk-why-cant-monkeys.html',
        comments='https://news.ycombinator.com/item?id=35431466',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_newscientist():
    d = build_hn_feed(
        title='San Francisco is getting cold feet about self-driving car tests',
        link='https://www.newscientist.com/article/2356888-san-francisco-is-getting-cold-feet-about-self-driving-car-tests/',
        comments='https://news.ycombinator.com/item?id=34608179',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_paulgraham():
    d = build_hn_feed(
        title='Why to start a startup in a bad economy (2008)',
        link='http://paulgraham.com/badeconomy.html',
        comments='https://news.ycombinator.com/item?id=34429869',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_sivers():
    d = build_hn_feed(
        title='Travelling Just for the People',
        link='https://sive.rs/travp',
        comments='https://news.ycombinator.com/item?id=34733694'
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_astral_codexten():
    d = build_hn_feed(
        title='Highlights from the Comments on IRBs',
        link='https://astralcodexten.substack.com/p/highlights-from-the-comments-on-irbs',
        comments='https://news.ycombinator.com/item?id=35608036',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_noahpinion():
    d = build_hn_feed(
        title='“Luxury” construction causes high rents like umbrellas cause rain',
        link='https://noahpinion.substack.com/p/luxury-construction-causes-high-rents',
        comments='https://news.ycombinator.com/item?id=35668072',
    )
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


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
