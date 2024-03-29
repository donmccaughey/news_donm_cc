import logging
from datetime import datetime,timezone
from email import utils

from feedparser import FeedParserDict, parse
from requests import ConnectTimeout

from news.url import URL
from .feed import Feed


def test_eq_and_hash():
    feed1 = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    feed1_dup = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    feed2 = Feed('Lobsters', 'lob', URL('https://lobste.rs/rss'))

    assert feed1 == feed1_dup
    assert hash(feed1) == hash(feed1_dup)

    assert feed1 != feed2


def test_str_and_repr():
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    assert str(feed) == 'Hacker News'
    assert repr(feed) == "Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))"


def test_entry_has_keys():
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    entry = {}

    assert not feed.entry_has_keys(entry, ['link', 'title'])

    entry = {'link': 'https://example.com/stuff'}

    assert not feed.entry_has_keys(entry, ['link', 'title'])

    entry = {'link': 'https://example.com/stuff', 'title': 'Stuff'}

    assert feed.entry_has_keys(entry, ['link', 'title'])


def test_is_entry_valid():
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    entry = {}

    assert not feed.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff'}

    assert not feed.is_entry_valid(entry)

    entry = {'link': 'https://example.com/stuff', 'title': 'Stuff'}

    assert feed.is_entry_valid(entry)


def test_is_recent_published_now():
    now = datetime.fromisoformat('2023-01-31T05:34:20+00:00')
    ago = now
    pub_date = utils.format_datetime(ago)
    xml = f'''
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
    d: FeedParserDict = parse(xml)
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    assert feed.is_entry_recent(d.entries[0], now)


def test_is_recent_published_14_days_ago():
    now = datetime.fromisoformat('2023-01-16T05:34:20+00:00')
    ago = datetime.fromisoformat('2023-01-02T05:34:20+00:00')
    pub_date = utils.format_datetime(ago)
    xml = f'''
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
    d: FeedParserDict = parse(xml)
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    assert feed.is_entry_recent(d.entries[0], now)


def test_is_recent_published_15_days_ago():
    now = datetime.fromisoformat('2023-01-16T05:34:20+00:00')
    ago = datetime.fromisoformat('2023-01-01T05:34:20+00:00')
    pub_date = utils.format_datetime(ago)
    xml = f'''
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
    d: FeedParserDict = parse(xml)
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    assert not feed.is_entry_recent(d.entries[0], now)


def test_is_recent_when_published_is_in_the_future(caplog):
    now = datetime.fromisoformat('2023-11-02T22:05:03.020862+00:00')
    xml = f'''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <title>Behind the Scenes of Apple’s Behind the Scenes of the ‘Scary Fast’ Keynote Film</title>
            <link rel="alternate" type="text/html" href="https://www.youtube.com/watch?v=y_E2okzJCvY"/>
            <link rel="shorturl" type="text/html" href="http://df4.us/v4d"/>
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2023/11/02/tobin-bts-scary-fast"/>
            <id>tag:daringfireball.net,2023:/linked//6.40333</id>
            <published>2023-11-02T23:01:32Z</published>
            <updated>2023-11-02T23:57:44Z</updated>
            <content type="html" xml:base="https://daringfireball.net/linked/" xml:lang="en"><![CDATA[...]]></content>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(xml)
    feed = Feed('Daring Fireball', 'df', URL('https://daringfireball.net/feeds/main'))

    assert feed.is_entry_recent(d.entries[0], now)
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == (
        'Daring Fireball entry "Behind the Scenes of Apple’s Behind the Scenes of the ‘Scary Fast’ Keynote Film" '
        'has a published date in the future: '
        'now = 2023-11-02 22:05:03.020862+00:00, '
        'published = 2023-11-02 23:01:32+00:00, '
        'skew = 0:56:28.979138'
    )


def test_is_recent_is_missing():
    xml = '''
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
    d: FeedParserDict = parse(xml)
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    assert feed.is_entry_recent(d.entries[0], datetime.now(timezone.utc))


class FakeResponse:
    def __init__(self, status_code, location=None):
        self.content = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <rss version="2.0">
                <channel>
                    <item>
                        <title>Entry 1</title>
                        <link>https://example.com/entry1</link>
                    </item>
                    <item>
                        <title>Entry 2</title>
                        <link>https://example.com/entry2</link>
                    </item>
                </channel>
            </rss>
            '''.encode('utf-8')
        self.headers = {}
        if location:
            self.headers['Location'] = location
        self.status_code = status_code


def make_get_function(*, exception=None, location=None, status_code=200):
    def fake_get(*args, **kwargs):
        if exception:
            raise exception
        return FakeResponse(status_code=status_code, location=location)
    return fake_get


def test_get_items_for_200_status(caplog, monkeypatch):
    monkeypatch.setattr('requests.get', make_get_function(status_code=200))

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(caplog.messages) is 0
    assert len(items) is 2


def test_get_items_for_302_status(caplog, monkeypatch):
    monkeypatch.setattr('requests.get', make_get_function(status_code=302))

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(caplog.messages) is 0
    assert len(items) is 2


def test_get_items_for_304_status(caplog, monkeypatch):
    monkeypatch.setattr('requests.get', make_get_function(status_code=304))

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(caplog.messages) is 0
    assert len(items) is 0


def test_get_items_for_308_status(caplog, monkeypatch):
    monkeypatch.setattr(
        'requests.get',
        make_get_function(status_code=308, location='https://example.com/redirect')
    )

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News returned status code 308: https://example.com/redirect'


def test_get_items_for_other_status(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('requests.get', make_get_function(status_code=500))

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News returned status code 500'


def test_get_items_if_requests_raises_exception(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('requests.get', make_get_function(exception=ConnectTimeout()))

    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    items = feed.get_items(datetime.now(timezone.utc))

    assert len(items) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News failed: ConnectTimeout()'


def test_parse_entries():
    xml = '''
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
    d: FeedParserDict = parse(xml)
    feed = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    items = feed.parse_entries(d.entries, datetime.now(timezone.utc))

    assert len(items) == 1
    assert items[0].title == 'Valid entry'


def test_update_from_with_etag_and_last_modified():
    feed1 = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    feed1_dup = Feed(
        'Hacker News', 'hn', URL('https://news.ycombinator.com/rss'),
        etag='W/"647aab77-10117"',
        last_modified='Sat, 03 Jun 2023 02:54:47 GMT',
    )

    feed1.update_from(feed1_dup)

    assert feed1.etag == 'W/"647aab77-10117"'
    assert feed1.last_modified == 'Sat, 03 Jun 2023 02:54:47 GMT'


def test_update_from_without_etag_and_last_modified():
    feed1 = Feed(
        'Hacker News', 'hn', URL('https://news.ycombinator.com/rss'),
        etag='W/"647aab77-10117"',
        last_modified='Sat, 03 Jun 2023 02:54:47 GMT',
    )
    feed1_dup = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))

    feed1.update_from(feed1_dup)

    assert feed1.etag == 'W/"647aab77-10117"'
    assert feed1.last_modified == 'Sat, 03 Jun 2023 02:54:47 GMT'


def test_decode_without_etag_and_last_modified():
    encoded = {
        'name': 'Example',
        'initials': 'ex',
    }

    feed = Feed.decode(encoded)

    assert feed.name == 'Example'
    assert feed.initials == 'ex'
    assert feed.url is None
    assert feed.etag is None
    assert feed.last_modified is None


def test_decode_with_etag_and_last_modified():
    encoded = {
        'name': 'Example',
        'initials': 'ex',
        'etag': 'W/"647aab77-10117"',
        'last_modified': 'Sat, 03 Jun 2023 02:54:47 GMT',
    }

    feed = Feed.decode(encoded)

    assert feed.name == 'Example'
    assert feed.initials == 'ex'
    assert feed.url is None
    assert feed.etag == 'W/"647aab77-10117"'
    assert feed.last_modified == 'Sat, 03 Jun 2023 02:54:47 GMT'


def test_encode_without_etag_and_last_modified():
    feed = Feed('Example', 'ex', URL('https://example.com/feed'))

    encoded = feed.encode()

    assert encoded['name'] == 'Example'
    assert encoded['initials'] == 'ex'
    assert 'url' not in encoded
    assert 'etag' not in encoded
    assert 'last_modified' not in encoded


def test_encode_with_etag_and_last_modified():
    feed = Feed(
        'Example', 'ex', URL('https://example.com/feed'),
        etag='W/"647aab77-10117"',
        last_modified='Sat, 03 Jun 2023 02:54:47 GMT',
    )

    encoded = feed.encode()

    assert encoded['name'] == 'Example'
    assert encoded['initials'] == 'ex'
    assert 'url' not in encoded
    assert encoded['etag'] == 'W/"647aab77-10117"'
    assert encoded['last_modified'] == 'Sat, 03 Jun 2023 02:54:47 GMT'
