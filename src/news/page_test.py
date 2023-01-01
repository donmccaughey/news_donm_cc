from .item import Item
from .news import News
from .page import Page
from .source import Source
from .url import URL


def test_no_news():
    news = News()
    page = Page(news, page_number=1, items_per_page=3)

    assert page.number == 1
    assert page.count == 0

    assert len(page) == 0
    assert list(page) == []

    assert page.previous is None
    assert page.next is None


def test_one_item():
    news = News([item1])
    page = Page(news, page_number=1, items_per_page=3)

    assert page.number == 1
    assert page.count == 1

    assert len(page) == 1
    assert list(page) == [item1]

    assert page.previous is None
    assert page.next is None


def test_two_items():
    news = News([item1, item2])
    page = Page(news, page_number=1, items_per_page=3)

    assert page.number == 1
    assert page.count == 1

    assert len(page) == 2
    assert list(page) == [item1, item2]

    assert page.previous is None
    assert page.next is None


def test_three_items():
    news = News([item1, item2, item3])
    page = Page(news, page_number=1, items_per_page=3)

    assert page.number == 1
    assert page.count == 1

    assert len(page) == 3
    assert list(page) == [item1, item2, item3]

    assert page.previous is None
    assert page.next is None


def test_four_items():
    news = News([item1, item2, item3, item4])
    page1 = Page(news, page_number=1, items_per_page=3)

    assert page1.number == 1
    assert page1.count == 2

    assert len(page1) == 3
    assert list(page1) == [item1, item2, item3]

    assert page1.previous is None

    page2 = page1.next
    assert page2 is not None

    assert page2.number == 2
    assert page2.count == 2

    assert len(page2) == 1
    assert list(page2) == [item4]

    assert page2.next is None

    page1 = page2.previous
    assert page1 is not None

    assert len(page1) == 3
    assert list(page1) == [item1, item2, item3]


def test_five_items():
    news = News([item1, item2, item3, item4, item5])
    page1 = Page(news, page_number=1, items_per_page=3)

    assert page1.number == 1
    assert page1.count == 2

    assert len(page1) == 3
    assert list(page1) == [item1, item2, item3]

    page2 = page1.next

    assert len(page2) == 2
    assert list(page2) == [item4, item5]

    assert page2.next is None
    assert page2.previous is not None


def test_six_items():
    news = News([item1, item2, item3, item4, item5, item6])
    page1 = Page(news, page_number=1, items_per_page=3)

    assert page1.number == 1
    assert page1.count == 2

    assert len(page1) == 3
    assert list(page1) == [item1, item2, item3]

    page2 = page1.next

    assert len(page2) == 3
    assert list(page2) == [item4, item5, item6]

    assert page2.next is None
    assert page2.previous is not None


def test_seven_items_backwards():
    news = News([item1, item2, item3, item4, item5, item6, item7])
    page3 = Page(news, page_number=3, items_per_page=3)

    assert page3.number == 3
    assert page3.count == 3

    assert len(page3) == 1
    assert list(page3) == [item7]

    page2 = page3.previous

    assert len(page2) == 3
    assert list(page2) == [item4, item5, item6]

    page1 = page2.previous

    assert len(page1) == 3
    assert list(page1) == [item1, item2, item3]

    assert page1.previous is None
    assert page1.next is not None


def test_page_number_past_end():
    news = News([item1, item2])
    page = Page(news, page_number=2, items_per_page=3)

    assert page.number == 2
    assert page.count == 1

    assert len(page) == 0
    assert list(page) == []

    assert page.previous is not None
    assert page.next is None


def test_str_and_repr():
    news = News([item1, item2, item3, item4])
    page = Page(news, page_number=1, items_per_page=3)

    assert str(page) == 'Page 1 of 2'
    assert repr(page) == '<Page 1 of 2, items[0:3]>'

    assert repr(page.next) == '<Page 2 of 2, items[3:4]>'


item1 = Item(
    URL('https://example.com/item1'), 'Item 1', Source(URL('https://source.com/1'), 'so')
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

item5 = Item(
    URL('https://example.com/item5'), 'Item 5', Source(URL('https://source.com/5'), 'so')
)

item6 = Item(
    URL('https://example.com/item6'), 'Item 6', Source(URL('https://source.com/6'), 'so')
)

item7 = Item(
    URL('https://example.com/item7'), 'Item 7', Source(URL('https://source.com/7'), 'so')
)
