from datetime import datetime, timezone
from feedparser import FeedParserDict, parse

from .hacker_news import HackerNews


def test_parse_entry_decodes_html_entities():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>&amp;lt;3 Deno</title>
                <link>https://matklad.github.io/2023/02/12/a-love-letter-to-deno.html</link>
                <comments>https://news.ycombinator.com/item?id=34767795</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == '<3 Deno'


def test_parse_entry_decodes_hex_char_entities():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>NameCheap&amp;#x27;s email hacked to send Metamask, DHL phishing emails</title>
                <link>https://www.bleepingcomputer.com/news/security/namecheaps-email-hacked-to-send-metamask-dhl-phishing-emails/</link>
                <comments>https://news.ycombinator.com/item?id=34768550</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()
    item = hn.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == "NameCheap's email hacked to send Metamask, DHL phishing emails"


def test_keep_entry_keeps_typical_entry():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>Can Doom Run It? An Adding Machine in Doom</title>
                <link>https://blog.otterstack.com/posts/202212-doom-calculator/</link>
                <comments>https://news.ycombinator.com/item?id=34102419</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()

    assert hn.keep_entry(entry)


def test_keep_entry_rejects_elpais():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>If Parrots Can Talk, Why Can’t Monkeys?</title>
                <link>https://english.elpais.com/science-tech/2023-01-10/if-parrots-can-talk-why-cant-monkeys.html</link>
                <comments>https://news.ycombinator.com/item?id=35431466</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_newscientist():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>San Francisco is getting cold feet about self-driving car tests</title>
                <link>https://www.newscientist.com/article/2356888-san-francisco-is-getting-cold-feet-about-self-driving-car-tests/</link>
                <comments>https://news.ycombinator.com/item?id=34608179</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_paulgraham():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>Why to start a startup in a bad economy (2008)</title>
                <link>http://paulgraham.com/badeconomy.html</link>
                <comments>https://news.ycombinator.com/item?id=34429869</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)


def test_keep_entry_rejects_sivers():
    feed = '''
    <rss version="2.0">
    	<channel>
            <item>
                <title>Travelling Just for the People</title>
                <link>https://sive.rs/travp</link>
                <comments>https://news.ycombinator.com/item?id=34733694</comments>
            </item>
    	</channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    hn = HackerNews()

    assert not hn.keep_entry(entry)
