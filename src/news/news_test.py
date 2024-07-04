from datetime import datetime, timedelta, timezone
from pytest import fixture

from .item import Item
from .news import News
from .source import Source
from .url import NormalizedURL


def test_str_and_repr(item1, item2, item3):
    news = News([item1, item2, item3])

    assert str(news) == '3 news items'
    assert repr(news) == '<News: 3 items>'


def test_update(item1, item2):
    news = News()

    new_count, modified_count = news.update([item1, item2], NOW)

    assert new_count == 2
    assert modified_count == 0
    assert len(news) == 2
    assert list(news) == [item1, item2]
    assert news.by_site == {'example.com': [item1], 'example.net': [item2]}


def test_update_for_empty():
    news = News()

    new_count, modified_count = news.update([], NOW)

    assert new_count == 0
    assert modified_count == 0


def test_update_for_all_duplicates(item1, item2, item3, item4):
    news = News([item1, item2, item3, item4])

    new_count, modified_count = news.update([item1, item2], NOW)

    assert new_count == 0
    assert modified_count == 2
    assert len(news) == 4
    assert news.by_site == {
            'example.com': [item1, item4],
            'example.net': [item2],
            'example.org': [item3]
        }


def test_update_for_some_duplicates(item1, item2, item3, item4):
    news = News([item1, item3, item4])

    new_count, modified_count = news.update([item1, item2], NOW)

    assert new_count == 1
    assert modified_count == 1
    assert len(news) == 4
    assert list(news) == [item2, item1, item3, item4]


def test_update_for_existing_item_from_new_source(item1, item1_alt_source):
    news = News([item1])

    new_count, modified_count = news.update([item1_alt_source], NOW)

    assert new_count == 0
    assert modified_count == 1
    assert len(news) == 1
    assert news.by_site == {'example.com': [item1]}
    assert len(news.ordered_items[0].sources) == 2
    assert item1.sources[0] in news.ordered_items[0].sources
    assert item1_alt_source.sources[0] in news.ordered_items[0].sources


def test_remove_old_when_empty():
    news = News(modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 0
    assert news.modified == AN_HOUR_AGO
    assert len(news) == 0


def test_remove_old_odd_1(item1_old, item2, item3):
    news = News([item3, item2, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 1
    assert news.modified == NOW
    assert len(news) == 2
    assert news.by_site == {'example.net': [item2], 'example.org': [item3]}


def test_remove_old_odd_2(item1_old, item2_old, item3):
    news = News([item3, item2_old, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 2
    assert news.modified == NOW
    assert len(news) == 1
    assert news.by_site == {'example.org': [item3]}


def test_remove_old_even_1(item1_old, item2, item3, item4):
    news = News([item4, item3, item2, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 1
    assert news.modified == NOW
    assert len(news) == 3
    assert news.by_site == {
            'example.net': [item2],
            'example.org': [item3],
            'example.com': [item4],
        }


def test_remove_old_even_2(item1_old, item2_old, item3, item4):
    news = News([item4, item3, item2_old, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 2
    assert news.modified == NOW
    assert len(news) == 2
    assert news.by_site == {
            'example.org': [item3],
            'example.com': [item4],
        }


def test_remove_old_when_none_expired(item1, item2, item3):
    news = News([item3, item2, item1], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 0
    assert news.modified == AN_HOUR_AGO
    assert news.by_site == {
            'example.com': [item1],
            'example.net': [item2],
            'example.org': [item3],
        }


def test_remove_old_when_all_expired(item1_old, item2_old):
    news = News([item2_old, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)

    old_count = news.remove_old(NOW)

    assert old_count == 2
    assert news.modified == NOW
    assert len(news) == 0
    assert news.by_site == {}


def test_remove_old_and_update_for_duplicate_item(item1, item1_old, item2, item3):
    news = News([item3, item2, item1_old], modified=AN_HOUR_AGO, lifetime=FIVE_DAYS)
    old_count = news.remove_old(NOW)

    assert old_count == 1

    new_count, modified_count = news.update([item1], NOW)

    assert new_count == 1
    assert modified_count == 0
    assert len(news) == 3


def test_search_when_empty():
    news = News()

    items = news.search('foo')

    assert items == []


def test_search_when_not_found(item1, item2, item3):
    news = News([item1, item2, item3])

    items = news.search('fnord')

    assert items == []


def test_search_for_one_term_with_one_match(item1, item2, item3):
    news = News([item1, item2, item3])

    items = news.search('1')

    assert items == [item1]


def test_search_preserves_item_order(item1, item2, item3):
    news = News([item1, item2, item3])

    items = news.search('Item')

    assert items == [item1, item2, item3]


def test_search_for_two_terms(item1, item1_old, item2, item2_old, item3, item4):
    news = News([item1_old, item2_old, item3, item4])

    items = news.search('Old Item')

    assert items == [item1, item2]


FIVE_DAYS = timedelta(days=5)
SIX_DAYS = timedelta(days=6)

NOW = datetime.now(timezone.utc)
AN_HOUR_AGO = NOW - timedelta(hours=1)
YESTERDAY = NOW - timedelta(days=1)
TWO_DAYS_AGO = NOW - timedelta(days=2)
THREE_DAYS_AGO = NOW - timedelta(days=3)

SIX_DAYS_AGO = NOW - timedelta(days=6)
SEVEN_DAYS_AGO = NOW - timedelta(days=7)


@fixture
def item1():
    return Item(
        NormalizedURL('https://example.com/item1'), 'Item 1',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        THREE_DAYS_AGO, THREE_DAYS_AGO
    )


@fixture
def item1_old():
    return Item(
        NormalizedURL('https://example.com/item1'), 'Item 1 Old',
        [Source(NormalizedURL('https://source.com/1'), 'so')],
        SEVEN_DAYS_AGO, SEVEN_DAYS_AGO
    )


@fixture
def item1_alt_source():
    return Item(
        NormalizedURL('https://example.com/item1'), 'Item 1',
        [Source(NormalizedURL('https://alt-source.com/2'), 'alt')],
        NOW, NOW
    )


@fixture
def item2():
    return Item(
        NormalizedURL('https://example.net/item2'), 'Item 2',
        [Source(NormalizedURL('https://source.com/2'), 'so')],
        TWO_DAYS_AGO, TWO_DAYS_AGO
    )


@fixture
def item2_old():
    return Item(
        NormalizedURL('https://example.net/item2'), 'Item 2 Old',
        [Source(NormalizedURL('https://source.com/2'), 'so')],
        SIX_DAYS_AGO, SIX_DAYS_AGO
    )


@fixture
def item3():
    return Item(
        NormalizedURL('https://example.org/item3'), 'Item 3',
        [Source(NormalizedURL('https://source.com/3'), 'so')],
        YESTERDAY, YESTERDAY
    )


@fixture
def item4():
    return Item(
        NormalizedURL('https://example.com/item4'), 'Item 4',
        [Source(NormalizedURL('https://source.com/4'), 'so')],
        AN_HOUR_AGO, AN_HOUR_AGO
    )


@fixture
def item5():
    return Item(
        NormalizedURL('https://example.com/item5'), 'Item 5',
        [Source(NormalizedURL('https://source.com/5'), 'so')],
        NOW, NOW
    )
