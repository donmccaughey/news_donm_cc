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


def test_remove_old_when_empty():
    news = News(lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 0
    assert not news.is_modified
    assert len(news) == 0


def test_remove_old_odd_1():
    news = News([item3, item2, item1_old], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 1
    assert news.is_modified
    assert len(news) == 2


def test_remove_old_odd_2():
    news = News([item3, item2_old, item1_old], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 2
    assert news.is_modified
    assert len(news) == 1


def test_remove_old_even_1():
    news = News([item4, item3, item2, item1_old], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 1
    assert news.is_modified
    assert len(news) == 3


def test_remove_old_even_2():
    news = News([item4, item3, item2_old, item1_old], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 2
    assert news.is_modified
    assert len(news) == 2


def test_remove_old_when_none_expired():
    news = News([item3, item2, item1], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 0
    assert not news.is_modified


def test_remove_old_when_all_expired():
    news = News([item2_old, item1_old], lifetime=FIVE_DAYS)

    old_count = news.remove_old()

    assert old_count == 2
    assert news.is_modified
    assert len(news) == 0


def test_remove_old_and_add_new_duplicate_item():
    news = News([item3, item2, item1_old], lifetime=FIVE_DAYS)
    old_count = news.remove_old()

    assert old_count == 1

    new_count = news.add_new(News([item1]))

    assert new_count == 1
    assert len(news) == 3


FIVE_DAYS = timedelta(days=5)
SIX_DAYS = timedelta(days=6)

TODAY = datetime.now(timezone.utc)
YESTERDAY = TODAY - timedelta(days=1)
TWO_DAYS_AGO = TODAY - timedelta(days=2)
THREE_DAYS_AGO = TODAY - timedelta(days=3)

SIX_DAYS_AGO = TODAY - timedelta(days=6)
SEVEN_DAYS_AGO = TODAY - timedelta(days=7)

item1 = Item(
    URL('https://example.com/item1'), 'Item 1', Source(URL('https://source.com/1'), 'so'),
    THREE_DAYS_AGO, THREE_DAYS_AGO
)

item1_old = Item(
    URL('https://example.com/item1'), 'Item 1 Old', Source(URL('https://source.com/1'), 'so'),
    SEVEN_DAYS_AGO, SEVEN_DAYS_AGO
)

item2 = Item(
    URL('https://example.com/item2'), 'Item 2', Source(URL('https://source.com/2'), 'so'),
    TWO_DAYS_AGO, TWO_DAYS_AGO
)

item2_old = Item(
    URL('https://example.com/item2'), 'Item 2 Old', Source(URL('https://source.com/2'), 'so'),
    SIX_DAYS_AGO, SIX_DAYS_AGO
)

item3 = Item(
    URL('https://example.com/item3'), 'Item 3', Source(URL('https://source.com/3'), 'so'),
    YESTERDAY, YESTERDAY
)

item4 = Item(
    URL('https://example.com/item4'), 'Item 4', Source(URL('https://source.com/4'), 'so'),
    TODAY, TODAY
)
