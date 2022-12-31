from feedparser import FeedParserDict, parse

from .site import Site, DaringFireball
from .url import URL


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


def test_df_keep_entry():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://daringfireball.net/2022/11/twitter_tumult" />
            <title>★ Twitter Tumult</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert df.keep_entry(entry)


def test_df_keep_entry_linked():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying" />
            <title>TikTok Spied on Forbes Journalists</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert df.keep_entry(entry)


def test_df_keep_entry_no_title():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying" />
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_df_keep_entry_no_links():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <title>TikTok Spied on Forbes Journalists</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_df_keep_entry_sponsors_link():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://retool.com/?utm_source=sponsor&amp;utm_medium=newsletter&amp;utm_campaign=daringfireball" />
            <link rel="related" type="text/html" href="https://daringfireball.net/feeds/sponsors/2022/12/retool_5" />
            <title>[Sponsor] Retool</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def test_df_keep_entry_the_talk_show_link():
    feed = '''
    <?xml version="1.0" encoding="utf-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <link rel="alternate" type="text/html" href="https://daringfireball.net/thetalkshow/2022/12/22/ep-365" />
            <link rel="related" type="text/html" href="https://daringfireball.net/linked/2022/12/22/the-talk-show-365" />
            <title>The Talk Show: ‘Permanent September’</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)
