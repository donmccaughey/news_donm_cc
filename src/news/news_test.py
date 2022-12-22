from datetime import datetime, timedelta, timezone

from .item import Item
from .news import News
from .url import URL


def test_add_new():
    news = News()
    empty_news = News()
    new_news1 = News([item1, item2])
    new_news2 = News([item3, item4])

    assert not news.is_modified

    news.add_new(empty_news)

    assert not news.is_modified

    news.add_new(new_news1)

    assert news.is_modified
    assert len(news) == 2
    assert list(news) == [item2, item1]

    news.is_modified = False
    news.add_new(new_news2)

    assert news.is_modified
    assert len(news) == 4
    assert list(news) == [item4, item3, item2, item1]


def test_remove_old():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=5)
    old = now - timedelta(days=6)
    old_item = Item(URL('https://example.com/item-old'), 'Old Item', URL('https://source.com/old'), created=old, modified=old)

    news = News([item1, old_item, item2])

    assert not news.is_modified
    assert len(news) == 3

    news.remove_old(cutoff)

    assert news.is_modified
    assert len(news) == 2

    news.is_modified = False
    news.remove_old(cutoff)

    assert not news.is_modified
    assert len(news) == 2


item1 = Item(
    URL('https://example.com/item1'), 'Item 1', URL('https://source.com/1')
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
