import pytest
from feedparser import FeedParserDict, parse
from pytest import mark

from .daring_fireball import DaringFireball


def test_is_entry_valid_rejects_no_title():
    d = build_df_feed(
        alternate='https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/',
        related='https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying',
        title='',
    )
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.is_entry_valid(entry)


def test_is_entry_valid_rejects_no_links():
    d = build_df_feed('', '', 'TikTok Spied on Forbes Journalists')
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.is_entry_valid(entry)


ACCEPT_SITE_TESTS = [
    pytest.param(
        'https://daringfireball.net/2022/11/twitter_tumult',
        '',
        '★ Twitter Tumult',
        id='essay',
    ),
    pytest.param(
        'https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/',
        'https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying',
        'TikTok Spied on Forbes Journalists',
        id='link',
    ),
]


@mark.parametrize('alternate, related, title', ACCEPT_SITE_TESTS)
def test_keep_entry_accepts_link(alternate, related, title):
    d = build_df_feed(
        alternate='https://daringfireball.net/2022/11/twitter_tumult',
        related='',
        title='★ Twitter Tumult',
    )
    entry = d.entries[0]
    df = DaringFireball()

    assert df.keep_entry(entry)


REJECT_SITE_TESTS = [
    pytest.param(
        'https://workos.com/?utm_source=daringfireball&amp;utm_medium=newsletter&amp;utm_campaign=df2023',
        'https://daringfireball.net/linked/2023/02/12/workos',
        'WorkOS',
        id='linked sponsor',
    ),
    pytest.param(
        'https://daringfireball.net/feeds/sponsors/',
        'https://daringfireball.net/linked/2023/04/22/df-sponsorship-openings',
        'DF Sponsorship Openings',
        id='sponsors alternate link',
    ),
    pytest.param(
        'https://retool.com/?utm_source=sponsor&amp;utm_medium=newsletter&amp;utm_campaign=daringfireball',
        'https://daringfireball.net/feeds/sponsors/2022/12/retool_5',
        '[Sponsor] Retool',
        id='sponsors related link',
    ),
    pytest.param(
        'https://daringfireball.net/thetalkshow/2022/12/22/ep-365',
        'https://daringfireball.net/linked/2022/12/22/the-talk-show-365',
        'The Talk Show: ‘Permanent September’',
        id='The Talk Show link',
    ),
    pytest.param(
        'https://dithering.fm/',
        'https://daringfireball.net/linked/2023/02/03/dithering',
        'Dithering',
        id='Dithering link',
    ),
]


@mark.parametrize('alternate, related, title', REJECT_SITE_TESTS)
def test_keep_entry_rejects_link(alternate, related, title):
    d = build_df_feed(str(alternate), str(related), str(title))
    entry = d.entries[0]
    df = DaringFireball()

    assert not df.keep_entry(entry)


def build_df_feed(alternate: str, related: str, title: str) -> FeedParserDict:
    feed = [
        '<?xml version="1.0" encoding="utf-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        '<entry>',
    ]
    if alternate:
        feed.append(f'<link rel="alternate" type="text/html" href="{alternate}"/>')
    if related:
        feed.append(f'<link rel="related" type="text/html" href="{related}"/>')
    if title:
        feed.append(f'<title>{title}</title>')
    feed += [
        '</entry>',
        '</feed>',
    ]
    return parse('\n'.join(feed))
