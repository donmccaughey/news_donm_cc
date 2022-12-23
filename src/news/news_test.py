from datetime import datetime, timedelta, timezone

from .item import Item
from .news import News
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

    news.add_new(News([item1, item2]))

    assert news.is_modified
    assert len(news) == 2
    assert list(news) == [item2, item1]


def test_add_new_for_empty():
    news = News()

    news.add_new(News())

    assert not news.is_modified


def test_add_new_for_all_duplicates():
    news = News([item1, item2, item3, item4])

    news.add_new(News([item1, item2]))

    assert not news.is_modified
    assert len(news) == 4


def test_add_new_for_some_duplicates():
    news = News([item1, item3, item4])

    news.add_new(News([item1, item2]))

    assert news.is_modified
    assert len(news) == 4
    assert list(news) == [item2, item1, item3, item4]


def test_remove_old():
    news = News([item3, item1_old, item2])
    now = datetime.now(timezone.utc)

    news.remove_old(now - FIVE_DAYS)

    assert news.is_modified
    assert len(news) == 2


def test_remove_old_when_none_expired():
    now = datetime.now(timezone.utc)
    news = News([item3, item1, item2])

    news.remove_old(now - FIVE_DAYS)

    assert not news.is_modified


def test_remove_old_and_add_new_duplicate_item():
    now = datetime.now(timezone.utc)
    news = News([item3, item1_old, item2])
    news.remove_old(now - FIVE_DAYS)

    news.add_new(News([item1]))

    assert len(news) == 3


FIVE_DAYS = timedelta(days=5)
SIX_DAYS = timedelta(days=6)

item1 = Item(
    URL('https://example.com/item1'), 'Item 1', URL('https://source.com/1')
)

item1_old = Item(
    URL('https://example.com/item1'), 'Item 1', URL('https://source.com/1'),
    item1.created - SIX_DAYS, item1.modified - SIX_DAYS
)

item2 = Item(
    URL('https://example.com/item2'), 'Item 2', URL('https://source.com/2')
)

item3 = Item(
    URL('https://example.com/item3'), 'Item 3', URL('https://source.com/3')
)

item4 = Item(
    URL('https://example.com/item4'), 'Item 4', URL('https://source.com/4')
)
