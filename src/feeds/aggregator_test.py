from datetime import datetime, timezone

from news.url import URL
from .aggregator import Aggregator
from feedparser import FeedParserDict, parse


def test_parse_entry_decodes_html_entities():
    d = build_feed(
        title='&amp;lt;3 Deno',
        link='https://matklad.github.io/2023/02/12/a-love-letter-to-deno.html',
        comments='https://news.ycombinator.com/item?id=34767795',
    )
    entry = d.entries[0]
    ag = Aggregator('Ag', 'ag', URL('https://rss.example.com'))
    item = ag.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == '<3 Deno'


def test_parse_entry_decodes_hex_char_entities():
    d = build_feed(
        title='NameCheap&amp;#x27;s email hacked to send Metamask, DHL phishing emails',
        link='https://www.bleepingcomputer.com/news/security/namecheaps-email-hacked-to-send-metamask-dhl-phishing-emails/',
        comments='https://news.ycombinator.com/item?id=34768550',
    )
    entry = d.entries[0]
    ag = Aggregator('Ag', 'ag', URL('https://rss.example.com'))
    item = ag.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == "NameCheap's email hacked to send Metamask, DHL phishing emails"


def build_feed(title: str, link: str, comments: str) -> FeedParserDict:
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
