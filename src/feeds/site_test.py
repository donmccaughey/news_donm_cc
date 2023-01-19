from datetime import datetime
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
