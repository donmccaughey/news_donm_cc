from news import URL
from .feeds import Feeds
from .feed import Feed


def test_init_empty():
    feeds = Feeds()

    assert len(feeds) == 0
    assert list(feeds) == []


def test_init():
    feed1 = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    feed2 = Feed('Lobsters', 'lob', URL('https://lobste.rs/rss'))
    feeds = Feeds([feed1, feed2])

    assert len(feeds) == 2
    assert list(feeds) == [feed1, feed2]


def test_update_from():
    feed1 = Feed('Hacker News', 'hn', URL('https://news.ycombinator.com/rss'))
    feed2 = Feed('Lobsters', 'lob', URL('https://lobste.rs/rss'))
    feeds = Feeds([feed1, feed2])

    feed1_dup = Feed(
        'Hacker News', 'hn', URL('https://news.ycombinator.com/rss'),
        etag='W/"647aab77-10117"',
    )
    feeds_dup = Feeds([feed1_dup])

    feeds.update_from(feeds_dup)

    assert len(feeds) == 2
    assert feed1.etag == 'W/"647aab77-10117"'
    assert feed2.etag is None


def test_decode():
    encoded = [
        {
            'name': 'Example1',
            'initials': 'ex1',
        },
        {
            'name': 'Example2',
            'initials': 'ex2',
            'etag': 'W/"647aab77-10117"',
        },
    ]

    feeds = Feeds.decode(encoded)

    assert len(feeds) == 2

    feeds_list = list(feeds)

    assert feeds_list[0].name == 'Example1'
    assert feeds_list[0].etag is None

    assert feeds_list[1].name == 'Example2'
    assert feeds_list[1].etag == 'W/"647aab77-10117"'


def test_encode():
    feed1 = Feed(
        'Hacker News', 'hn', URL('https://news.ycombinator.com/rss'),
        etag='W/"647aab77-10117"',
    )
    feed2 = Feed('Lobsters', 'lob', URL('https://lobste.rs/rss'))
    feeds = Feeds([feed1, feed2])

    encoded = feeds.encode()

    assert len(encoded) == 2
    assert encoded[0]['name'] == 'Hacker News'
    assert encoded[0]['etag'] == 'W/"647aab77-10117"'
    assert encoded[1]['name'] == 'Lobsters'
    assert encoded[1].get('etag') is None
