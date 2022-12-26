from datetime import datetime, timedelta, timezone

from .item import Item
from .news import News
from .source import Source
from .url import URL


def test_str_and_repr():
    news = News([item1, item2, item3])

    assert str(news) == '3 news items'
    assert repr(news) == '<News: 3 items>'

    news.is_modified = True

    assert str(news) == '3 news items (modified)'
    assert repr(news) == '<News: 3 items, modified>'


def test_add_new():
    news = News()

    new_count = news.add_new(News([item1, item2]))

    assert new_count == 2
    assert news.is_modified
    assert len(news) == 2
    assert list(news) == [item2, item1]


def test_add_new_for_empty():
    news = News()

    new_count = news.add_new(News())

    assert new_count == 0
    assert not news.is_modified


def test_add_new_for_all_duplicates():
    news = News([item1, item2, item3, item4])

    new_count = news.add_new(News([item1, item2]))

    assert new_count == 0
    assert not news.is_modified
    assert len(news) == 4


def test_add_new_for_some_duplicates():
    news = News([item1, item3, item4])

    new_count = news.add_new(News([item1, item2]))

    assert new_count == 1
    assert news.is_modified
    assert len(news) == 4
    assert list(news) == [item2, item1, item3, item4]


def test_remove_old():
    news = News([item3, item1_old, item2])
    now = datetime.now(timezone.utc)

    old_count = news.remove_old(now - FIVE_DAYS)

    assert old_count == 1
    assert news.is_modified
    assert len(news) == 2


def test_remove_old_when_none_expired():
    now = datetime.now(timezone.utc)
    news = News([item3, item1, item2])

    old_count = news.remove_old(now - FIVE_DAYS)

    assert old_count == 0
    assert not news.is_modified


def test_remove_old_and_add_new_duplicate_item():
    now = datetime.now(timezone.utc)
    news = News([item3, item1_old, item2])
    old_count = news.remove_old(now - FIVE_DAYS)

    assert old_count == 1

    new_count = news.add_new(News([item1]))

    assert new_count == 1
    assert len(news) == 3


FIVE_DAYS = timedelta(days=5)
SIX_DAYS = timedelta(days=6)

item1 = Item(
    URL('https://example.com/item1'), 'Item 1', Source(URL('https://source.com/1'), 'so')
)

item1_old = Item(
    URL('https://example.com/item1'), 'Item 1', Source(URL('https://source.com/1'), 'so'),
    item1.created - SIX_DAYS, item1.modified - SIX_DAYS
)

item2 = Item(
    URL('https://example.com/item2'), 'Item 2', Source(URL('https://source.com/2'), 'so')
)

item3 = Item(
    URL('https://example.com/item3'), 'Item 3', Source(URL('https://source.com/3'), 'so')
)

item4 = Item(
    URL('https://example.com/item4'), 'Item 4', Source(URL('https://source.com/4'), 'so')
)
