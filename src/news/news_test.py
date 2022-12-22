from datetime import datetime, timedelta, timezone

from .item import Item
from .news import News
from .url import URL


def test_iadd():
    news = News()
    new_news = News([
        Item(
            URL('https://example.com/item1'), 'Item 1', URL('https://source.com/1')
        ),
        Item(
            URL('https://example.com/item2'), 'Item 2', URL('https://source.com/2')
        ),
    ])
    empty_news = News()

    assert not news.is_modified

    news += empty_news

    assert not news.is_modified

    news += new_news

    assert news.is_modified
    assert 2 == len(news)


def test_prune():
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=5)
    old = now - timedelta(days=6)

    news = News ([
        Item(
            URL('https://example.com/item1'), 'Item 1', URL('https://source.com/1')
        ),
        Item(
            URL('https://example.com/item2'), 'Item 2', URL('https://source.com/2'),
            created=old, modified=old
        ),
    ])

    assert not news.is_modified

    news.prune(cutoff)

    assert news.is_modified
    assert 1 == len(news)
