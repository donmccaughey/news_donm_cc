from feedparser import FeedParserDict, parse

from .daring_fireball import DaringFireball


def test_keep_entry_keeps_essay():
    d = build_df_feed(
        alternate='https://daringfireball.net/2022/11/twitter_tumult',
        related='',
        title='★ Twitter Tumult',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert df.keep_entry(entry)


def test_keep_entry_keeps_linked():
    d = build_df_feed(
        alternate='https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/',
        related='https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying',
        title='TikTok Spied on Forbes Journalists',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert df.keep_entry(entry)


def test_keep_entry_rejects_linked_sponsor():
    d = build_df_feed(
        alternate='https://workos.com/?utm_source=daringfireball&amp;utm_medium=newsletter&amp;utm_campaign=df2023',
        related='https://daringfireball.net/linked/2023/02/12/workos',
        title='WorkOS',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.keep_entry(entry)


def test_is_entry_valid_rejects_no_title():
    d = build_df_feed(
        alternate='https://www.forbes.com/sites/emilybaker-white/2022/12/22/tiktok-tracks-forbes-journalists-bytedance/',
        related='https://daringfireball.net/linked/2022/12/22/tiktok-forbes-spying',
        title='',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.is_entry_valid(entry)


def test_is_entry_valid_rejects_no_links():
    d = build_df_feed('', '', 'TikTok Spied on Forbes Journalists')
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.is_entry_valid(entry)


def test_keep_entry_rejects_sponsors_alternate_link():
    d = build_df_feed(
        alternate='https://daringfireball.net/feeds/sponsors/',
        related='https://daringfireball.net/linked/2023/04/22/df-sponsorship-openings',
        title='DF Sponsorship Openings',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_sponsors_related_link():
    d = build_df_feed(
        alternate='https://retool.com/?utm_source=sponsor&amp;utm_medium=newsletter&amp;utm_campaign=daringfireball',
        related='https://daringfireball.net/feeds/sponsors/2022/12/retool_5',
        title='[Sponsor] Retool',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_the_talk_show_link():
    d = build_df_feed(
        alternate='https://daringfireball.net/thetalkshow/2022/12/22/ep-365',
        related='https://daringfireball.net/linked/2022/12/22/the-talk-show-365',
        title='The Talk Show: ‘Permanent September’',
    )
    entry = d.entries[0]
    df = DaringFireball({})

    assert not df.keep_entry(entry)


def test_keep_entry_rejects_dithering_link():
    d = build_df_feed(
        alternate='https://dithering.fm/',
        related='https://daringfireball.net/linked/2023/02/03/dithering',
        title='Dithering',
    )
    entry = d.entries[0]
    df = DaringFireball({})

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
