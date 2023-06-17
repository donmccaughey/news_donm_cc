import logging
from datetime import datetime,timezone
from email import utils

from feedparser import FeedParserDict, parse

from news import URL
from .site import Site


def test_str_and_repr():
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert str(site) == 'Hacker News'
    assert repr(site) == "Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')"


def test_entry_has_keys():
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    entry = {}

    assert not site.entry_has_keys(entry, ['link', 'title'])

    entry = {'link': 'https://example.com/stuff'}

    assert not site.entry_has_keys(entry, ['link', 'title'])

    entry = {'link': 'https://example.com/stuff', 'title': 'Stuff'}

    assert site.entry_has_keys(entry, ['link', 'title'])


def test_is_entry_valid():
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    entry = {}

    assert not site.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff'}

    assert not site.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff', 'title': 'Stuff'}

    assert site.is_entry_valid(entry)


def test_is_recent_published_now():
    now = datetime.fromisoformat('2023-01-31T05:34:20+00:00')
    ago = now
    pub_date = utils.format_datetime(ago)
    feed = f'''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Something or other</title>
                <link>https://example.com/something</link>
                <pubDate>{pub_date}</pubDate>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert site.is_entry_recent(d.entries[0], now)


def test_is_recent_published_14_days_ago():
    now = datetime.fromisoformat('2023-01-16T05:34:20+00:00')
    ago = datetime.fromisoformat('2023-01-02T05:34:20+00:00')
    pub_date = utils.format_datetime(ago)
    feed = f'''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Something or other</title>
                <link>https://example.com/something</link>
                <pubDate>{pub_date}</pubDate>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert site.is_entry_recent(d.entries[0], now)


def test_is_recent_published_15_days_ago():
    now = datetime.fromisoformat('2023-01-16T05:34:20+00:00')
    ago = datetime.fromisoformat('2023-01-01T05:34:20+00:00')
    pub_date = utils.format_datetime(ago)
    feed = f'''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Something or other</title>
                <link>https://example.com/something</link>
                <pubDate>{pub_date}</pubDate>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert not site.is_entry_recent(d.entries[0], now)


def test_is_recent_is_missing():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Something or other</title>
                <link>https://example.com/something</link>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    assert site.is_entry_recent(d.entries[0], datetime.now(timezone.utc))


class FakeFeedParserDict:
    def __init__(self, status, href=None):
        self.entries = []
        if status:
            self.status = status
        if href:
            self.href = href

    def __contains__(self, item):
        return hasattr(self, item)


def make_parse_function(status, href=None):
    def fake_parse(*args, **kwargs):
        return FakeFeedParserDict(status=status, href=href)
    return fake_parse


def test_get_items_for_missing_status(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=None))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News failed without status code'


def test_get_items_for_200_status(monkeypatch):
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=200))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0


def test_get_items_for_302_status(monkeypatch):
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=302))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0


def test_get_items_for_304_status(monkeypatch):
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=304))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0


def test_get_items_for_308_status(caplog, monkeypatch):
    parse_function = make_parse_function(status=308, href='https://example.com/redirect')
    monkeypatch.setattr('feeds.site.parse', parse_function)

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News returned status code 308: https://example.com/redirect'


def test_get_items_for_other_status(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=500))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    items = site.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News returned status code 500'


def test_parse_entries():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Valid entry</title>
                <link>https://example.com/valid</link>
            </item>
            <item>
                <title>Invalid entry</title>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')

    items = site.parse_entries(d.entries, datetime.now(timezone.utc))

    assert len(items) == 1
    assert items[0].title == 'Valid entry'
