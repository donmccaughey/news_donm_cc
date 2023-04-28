from feedparser import FeedParserDict, parse

from .streetsblog import Streetsblog


def test_keep_entry_todays_headlines():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Today&#8217;s Headlines</title>
                <link>https://sf.streetsblog.org/2023/01/03/todays-headlines-3375/</link>
                <category><![CDATA[Today's Headlines]]></category>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    sb = Streetsblog({})

    assert sb.keep_entry(entry)


def test_keep_entry_other_category():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>What It Takes to Put a Seat At Every Bus Stop in Town</title>
                <link>https://usa.streetsblog.org/2022/12/21/what-it-takes-to-put-a-seat-at-every-bus-stop-in-town/#new_tab</link>
                <category><![CDATA[Streetsblog.net]]></category>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    sb = Streetsblog({})

    assert not sb.keep_entry(entry)


def test_keep_entry_no_title():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <link>https://sf.streetsblog.org/2023/01/03/todays-headlines-3375/</link>
                <category><![CDATA[Today's Headlines]]></category>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    sb = Streetsblog({})

    assert not sb.keep_entry(entry)


def test_keep_entry_no_link():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Today&#8217;s Headlines</title>
                <category><![CDATA[Today's Headlines]]></category>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    sb = Streetsblog({})

    assert not sb.keep_entry(entry)


def test_keep_entry_no_category():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
        <channel>
            <item>
                <title>Today&#8217;s Headlines</title>
                <link>https://sf.streetsblog.org/2023/01/03/todays-headlines-3375/</link>
            </item>
        </channel>
    </rss>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    sb = Streetsblog({})

    assert not sb.keep_entry(entry)
