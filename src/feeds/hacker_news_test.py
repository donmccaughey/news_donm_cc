from feedparser import FeedParserDict, parse

from .hacker_news import HackerNews


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
