import logging
from datetime import datetime,timezone
from news import URL
from .site import Site, is_recent


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


class FakeEntry:
    def __init__(self, time_tuple):
        self.published_parsed = time_tuple


def test_is_recent():
    now = datetime.fromisoformat('2023-01-31T05:34:20+00:00')

    # 2023-01-31
    entry1 = FakeEntry(
        (2023, 1, 31, 5, 34, 20, 3, 31, 0)
    )
    assert is_recent(entry1, now)

    # 2023-01-02
    entry2 = FakeEntry(
        (2023, 1, 2, 5, 34, 20, 0, 2, 0)
    )
    assert is_recent(entry2, now)

    # 2023-01-01
    entry3 = FakeEntry(
        (2023, 1, 1, 5, 34, 20, 7, 1, 0)
    )
    assert not is_recent(entry3, now)


class FakeFeedParserDict:
    def __init__(self, status):
        self.entries = []
        if status:
            self.status = status

    def __contains__(self, item):
        return hasattr(self, item)


def make_parse_function(status):
    def parse(*args, **kwargs):
        return FakeFeedParserDict(status=status)
    return parse


def test_get_for_missing_status(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=None))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    news = site.get(datetime.now(timezone.utc))

    assert len(news) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News failed without status code'


def test_get_for_200_status(monkeypatch):
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=200))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    news = site.get(datetime.now(timezone.utc))

    assert len(news) is 0


def test_get_for_302_status(monkeypatch):
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=302))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    news = site.get(datetime.now(timezone.utc))

    assert len(news) is 0


def test_get_for_304_status(caplog, monkeypatch):
    caplog.set_level(logging.DEBUG)
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=304))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    news = site.get(datetime.now(timezone.utc))

    assert len(news) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News is unmodified'


def test_get_for_other_status(caplog, monkeypatch):
    caplog.set_level(logging.WARNING)
    monkeypatch.setattr('feeds.site.parse', make_parse_function(status=500))

    site = Site(URL('https://news.ycombinator.com/rss'), 'Hacker News', 'hn')
    news = site.get(datetime.now(timezone.utc))

    assert len(news) is 0
    assert len(caplog.messages) is 1
    assert caplog.messages[0] == 'Hacker News returned status code 500'
