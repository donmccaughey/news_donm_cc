from datetime import datetime, timezone

import pytest
from feedparser import FeedParserDict, parse
from pytest import mark

from news.url import NormalizedURL, URL
from .reddit import extract_links, Reddit, is_reddit_media_link


FEED_URL = URL('https://www.reddit.com/.rss?feed=12345&user=alice')


def test_parse_entry_for_image_link():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <content type="html">&lt;table&gt; &lt;tr&gt;&lt;td&gt; &lt;a href=&quot;https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/&quot;&gt;
                &lt;img src=&quot;https://preview.redd.it/ylkzznbsfiwa1.jpg?width=640&amp;amp;crop=smart&amp;amp;auto=webp&amp;amp;v=enabled&amp;amp;s=8c32954c257d26068750c4e025d7d67b8fe80fd7&quot;
                alt=&quot;Spolia: repurposed Roman inscriptions in València, Spain (facade of the Basilica of Our Lady of
                the Forsaken)&quot; title=&quot;Spolia: repurposed Roman inscriptions in València, Spain (facade of the
                Basilica of Our Lady of the Forsaken)&quot; /&gt; &lt;/a&gt; &lt;/td&gt;&lt;td&gt; &amp;#32; submitted by
                &amp;#32; &lt;a href=&quot;https://www.reddit.com/user/jatsefos&quot;&gt; /u/jatsefos &lt;/a&gt; &amp;#32;
                to &amp;#32; &lt;a href=&quot;https://www.reddit.com/r/latin/&quot;&gt; r/latin &lt;/a&gt; &lt;br/&gt; &lt;span&gt;&lt;a
                href=&quot;https://i.redd.it/ylkzznbsfiwa1.jpg&quot;&gt;[link]&lt;/a&gt;&lt;/span&gt; &amp;#32; &lt;span&gt;&lt;a
                href=&quot;https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/&quot;&gt;[comments]&lt;/a&gt;&lt;/span&gt;
                &lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;
            </content>
            <link href="https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/"/>
            <title>Spolia: repurposed Roman inscriptions in València, Spain (facade of the Basilica of Our Lady of the Forsaken)</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    r = Reddit(FEED_URL)
    entry = d.entries[0]
    item = r.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == 'Spolia: repurposed Roman inscriptions in València, Spain (facade of the Basilica of Our Lady of the Forsaken)'
    assert item.url == NormalizedURL('https://old.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/')
    assert item.sources[0].url == URL('https://old.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/')
    assert item.sources[0].site_id == 'r/latin'


def test_parse_entry_for_gallery_link():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <content type="html">&lt;table&gt; &lt;tr&gt;&lt;td&gt; &lt;a href=&quot;https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/&quot;&gt;
                &lt;img src=&quot;https://b.thumbs.redditmedia.com/9v60oNakj5OiZi5Toa97iP_Bm5Mk4hV-3qAE0ng6zVA.jpg&quot;
                alt=&quot;Mini photo shoot with my Pyr Sushi&quot; title=&quot;Mini photo shoot with my Pyr Sushi&quot; /&gt;
                &lt;/a&gt; &lt;/td&gt;&lt;td&gt; &amp;#32; submitted by &amp;#32; &lt;a href=&quot;https://www.reddit.com/user/sitting-duckie&quot;&gt;
                /u/sitting-duckie &lt;/a&gt; &amp;#32; to &amp;#32; &lt;a href=&quot;https://www.reddit.com/r/greatpyrenees/&quot;&gt;
                r/greatpyrenees &lt;/a&gt; &lt;br/&gt; &lt;span&gt;&lt;a href=&quot;https://www.reddit.com/gallery/130qn68&quot;&gt;[link]&lt;/a&gt;&lt;/span&gt;
                &amp;#32; &lt;span&gt;&lt;a href=&quot;https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/&quot;&gt;[comments]&lt;/a&gt;&lt;/span&gt;
                &lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;
            </content>
            <link href="https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/"/>
            <title>Mini photo shoot with my Pyr Sushi</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    r = Reddit(FEED_URL)
    entry = d.entries[0]
    item = r.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == 'Mini photo shoot with my Pyr Sushi'
    assert item.url == NormalizedURL('https://old.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/')
    assert item.sources[0].url == URL('https://old.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/')
    assert item.sources[0].site_id == 'r/greatpyrenees'


def test_parse_entry_for_website_link():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <content type="html">&lt;table&gt; &lt;tr&gt;&lt;td&gt; &lt;a href=&quot;https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/&quot;&gt;
                &lt;img src=&quot;https://external-preview.redd.it/Ag_coVTTtZ813K5rsWexhBO6LYu-ZVJXQLk0naoEJkA.jpg?width=108&amp;amp;crop=smart&amp;amp;auto=webp&amp;amp;v=enabled&amp;amp;s=3b924e6f0eb9984dc137311a541e6d2b169aae2c&quot;
                alt=&quot;Report on surprise hyper CVE from 2023-04-11&quot; title=&quot;Report on surprise hyper CVE from
                2023-04-11&quot; /&gt; &lt;/a&gt; &lt;/td&gt;&lt;td&gt; &amp;#32; submitted by &amp;#32; &lt;a href=&quot;https://www.reddit.com/user/seanmonstar&quot;&gt;
                /u/seanmonstar &lt;/a&gt; &amp;#32; to &amp;#32; &lt;a href=&quot;https://www.reddit.com/r/rust/&quot;&gt;
                r/rust &lt;/a&gt; &lt;br/&gt; &lt;span&gt;&lt;a href=&quot;https://seanmonstar.com/post/715784167270596608/coe-surpise-hyper-cve&quot;&gt;[link]&lt;/a&gt;&lt;/span&gt;
                &amp;#32; &lt;span&gt;&lt;a href=&quot;https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/&quot;&gt;[comments]&lt;/a&gt;&lt;/span&gt;
                &lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;
            </content>
            <link href="https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/"/>
            <title>Report on surprise hyper CVE from 2023-04-11</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    r = Reddit(FEED_URL)
    entry = d.entries[0]
    item = r.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == 'Report on surprise hyper CVE from 2023-04-11'
    assert item.url == URL('https://seanmonstar.com/post/715784167270596608/coe-surpise-hyper-cve')
    assert item.sources[0].url == URL('https://old.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/')
    assert item.sources[0].site_id == 'r/rust'


def test_parse_entry_for_website_link_cleans_url():
    feed = '''
    <?xml version="1.0" encoding="UTF-8"?>
    <feed xmlns="http://www.w3.org/2005/Atom">
        <entry>
            <content type="html">&amp;#32; submitted by &amp;#32; &lt;a href=&quot;https://www.reddit.com/user/davetowers646&quot;&gt;
                /u/davetowers646 &lt;/a&gt; &amp;#32; to &amp;#32; &lt;a href=&quot;https://www.reddit.com/r/news/&quot;&gt;
                r/news &lt;/a&gt; &lt;br/&gt; &lt;span&gt;&lt;a href=&quot;https://apnews.com/article/how-many-people-smoke-us-64987fe2b7bf764c64d4594e5b02e6ea?utm_source=homepage&amp;amp;utm_medium=TopNews&amp;amp;utm_campaign=position_07&quot;&gt;[link]&lt;/a&gt;&lt;/span&gt;
                &amp;#32; &lt;span&gt;&lt;a href=&quot;https://www.reddit.com/r/news/comments/130kndv/us_adult_cigarette_smoking_rate_hits_new_alltime/&quot;&gt;[comments]&lt;/a&gt;&lt;/span&gt;
            </content>
            <link href="https://www.reddit.com/r/news/comments/130kndv/us_adult_cigarette_smoking_rate_hits_new_alltime/"/>
            <title>US adult cigarette smoking rate hits new all-time low</title>
        </entry>
    </feed>
    '''
    d: FeedParserDict = parse(feed)
    r = Reddit(FEED_URL)
    entry = d.entries[0]
    item = r.parse_entry(entry, datetime.now(timezone.utc))
    assert item.title == 'US adult cigarette smoking rate hits new all-time low'
    assert item.url == NormalizedURL('https://apnews.com/article/how-many-people-smoke-us-64987fe2b7bf764c64d4594e5b02e6ea')
    assert item.sources[0].url == URL('https://old.reddit.com/r/news/comments/130kndv/us_adult_cigarette_smoking_rate_hits_new_alltime/')
    assert item.sources[0].site_id == 'r/news'


EXTRACT_LINKS_TESTS = [
    pytest.param(
        '''<table> <tr><td> <a href="https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/">
            <img src="https://preview.redd.it/ylkzznbsfiwa1.jpg?width=640&amp;crop=smart&amp;auto=webp&amp;v=enabled&amp;s=8c32954c257d26068750c4e025d7d67b8fe80fd7"
            alt="Spolia: repurposed Roman inscriptions in València, Spain (facade of the Basilica of Our Lady of
            the Forsaken)" title="Spolia: repurposed Roman inscriptions in València, Spain (facade of the
            Basilica of Our Lady of the Forsaken)" /> </a> </td><td> &#32; submitted by
            &#32; <a href="https://www.reddit.com/user/jatsefos"> /u/jatsefos </a> &#32;
            to &#32; <a href="https://www.reddit.com/r/latin/"> r/latin </a> <br/> <span><a
            href="https://i.redd.it/ylkzznbsfiwa1.jpg">[link]</a></span> &#32; <span><a
            href="https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/">[comments]</a></span>
            </td></tr></table>''',
        NormalizedURL('https://default.com'),
        NormalizedURL('https://www.reddit.com/r/latin/comments/131102k/spolia_repurposed_roman_inscriptions_in_valència/'),
        id='image link',
    ),
    pytest.param(
        '''<table> <tr><td> <a href="https://www.reddit.com/r/aww/comments/130no54/six_little_fwinds/">
            <img src="https://external-preview.redd.it/np4f2qDRD-R8zaj5xJ-MZNkfpOItjdYPMfUKmu64E_Y.png?width=640&amp;crop=smart&amp;auto=webp&amp;v=enabled&amp;s=c69e2e49e86a2b6fbe3eeef8f9ae44f41220f141"
            alt="Six little fwinds" title="Six little fwinds" /> </a> </td><td>
            &#32; submitted by &#32; <a href="https://www.reddit.com/user/Unused_Application_">
            /u/Unused_Application_ </a> &#32; to &#32; <a href="https://www.reddit.com/r/aww/">
            r/aww </a> <br/> <span><a href="https://v.redd.it/i90hkj9nrfwa1">[link]</a></span>
            &#32; <span><a href="https://www.reddit.com/r/aww/comments/130no54/six_little_fwinds/">[comments]</a></span>
            </td></tr></table>''',
        NormalizedURL('https://default.com'),
        NormalizedURL('https://www.reddit.com/r/aww/comments/130no54/six_little_fwinds/'),
        id='video link',
    ),
    pytest.param(
        '''<table> <tr><td> <a href="https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/">
            <img src="https://b.thumbs.redditmedia.com/9v60oNakj5OiZi5Toa97iP_Bm5Mk4hV-3qAE0ng6zVA.jpg"
            alt="Mini photo shoot with my Pyr Sushi" title="Mini photo shoot with my Pyr Sushi" />
            </a> </td><td> &#32; submitted by &#32; <a href="https://www.reddit.com/user/sitting-duckie">
            /u/sitting-duckie </a> &#32; to &#32; <a href="https://www.reddit.com/r/greatpyrenees/">
            r/greatpyrenees </a> <br/> <span><a href="https://www.reddit.com/gallery/130qn68">[link]</a></span>
            &#32; <span><a href="https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/">[comments]</a></span>
            </td></tr></table>''',
        NormalizedURL('https://default.com'),
        NormalizedURL('https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/'),
        id='gallery link',
    ),
    pytest.param(
        '''<table> <tr><td> <a href="https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/">
            <img src="https://external-preview.redd.it/Ag_coVTTtZ813K5rsWexhBO6LYu-ZVJXQLk0naoEJkA.jpg?width=108&amp;crop=smart&amp;auto=webp&amp;v=enabled&amp;s=3b924e6f0eb9984dc137311a541e6d2b169aae2c"
            alt="Report on surprise hyper CVE from 2023-04-11" title="Report on surprise hyper CVE from
            2023-04-11" /> </a> </td><td> &#32; submitted by &#32; <a href="https://www.reddit.com/user/seanmonstar">
            /u/seanmonstar </a> &#32; to &#32; <a href="https://www.reddit.com/r/rust/">
            r/rust </a> <br/> <span><a href="https://seanmonstar.com/post/715784167270596608/coe-surpise-hyper-cve">[link]</a></span>
            &#32; <span><a href="https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/">[comments]</a></span>
            </td></tr></table>''',
        NormalizedURL('https://seanmonstar.com/post/715784167270596608/coe-surpise-hyper-cve'),
        NormalizedURL('https://www.reddit.com/r/rust/comments/13147i3/report_on_surprise_hyper_cve_from_20230411/'),
        id='website link',
    ),
    pytest.param(
        '''<!-- SC_OFF --><div class="md"><p>I am just about to hit the
            2023 Pre-Tax limit on my 401k, but my employer allows me to do after tax contributions (MBDR).</p>
            <p>I am allowed to contribute up to 65% of my paycheck to 401k contributions. My employer also
            provides an ESPP, where I can contribute up to 10% of my paycheck.</p> <p>So in total, I can
            contribute 75% of my paycheck to (post-tax) accounts. However, I expect that I will owe more than 25% of my
            paycheck to federal, state, and SS taxes. What should I expect to happen if I were to actually contribute
            the maximum amount? Would I get a negative paycheck?</p> </div><!-- SC_ON --> &#32;
            submitted by &#32; <a href="https://www.reddit.com/user/Enzyesha"> /u/Enzyesha </a>
            &#32; to &#32; <a href="https://www.reddit.com/r/financialindependence/">
            r/financialindependence </a> <br/> <span><a href="https://www.reddit.com/r/financialindependence/comments/130zdm6/could_contributing_too_much_of_my_paycheck_to/">[link]</a></span>
            &#32; <span><a href="https://www.reddit.com/r/financialindependence/comments/130zdm6/could_contributing_too_much_of_my_paycheck_to/">[comments]</a></span>''',
        NormalizedURL('https://www.reddit.com/r/financialindependence/comments/130zdm6/could_contributing_too_much_of_my_paycheck_to/'),
        NormalizedURL('https://www.reddit.com/r/financialindependence/comments/130zdm6/could_contributing_too_much_of_my_paycheck_to/'),
        id='discussion',
    ),
    pytest.param(
        '''&#32; submitted by &#32; <a href="https://www.reddit.com/user/CyborgPrime"> /u/CyborgPrime </a> 
            &#32; to &#32; <a href="https://www.reddit.com/r/traveller/"> r/traveller </a> <br /> 
            <span><a href="/r/u_CyborgPrime/comments/16cv0ek/is_starfield_like_traveller/">[link]</a></span> 
            &#32; <span><a href="https://www.reddit.com/r/traveller/comments/16dusai/is_starfield_like_traveller/">[comments]</a></span>''',
        NormalizedURL('https://www.reddit.com/user/CyborgPrime/comments/16cv0ek/is_starfield_like_traveller/'),
        NormalizedURL('https://www.reddit.com/r/traveller/comments/16dusai/is_starfield_like_traveller/'),
        id='user comments',
    )
]


@mark.parametrize('content, expected_link, expected_comments', EXTRACT_LINKS_TESTS)
def test_extract_links(content, expected_link, expected_comments):
    link, comments = extract_links(
        content, default=NormalizedURL('https://default.com')
    )

    assert link == expected_link
    assert comments == expected_comments


REJECT_SITE_TESTS = [
    pytest.param(
        'If Parrots Can Talk, Why Can’t Monkeys?',
        'https://english.elpais.com/science-tech/2023-01-10/if-parrots-can-talk-why-cant-monkeys.html',
        'https://news.ycombinator.com/item?id=35431466',
        id='english.elpais.com',
    ),
]


@mark.parametrize('title, link, comments', REJECT_SITE_TESTS)
def test_keep_item_rejects_site(title, link, comments):
    d = build_reddit_feed(str(title), str(link), str(comments))
    entry = d.entries[0]
    r = Reddit(FEED_URL)
    item = r.parse_entry(entry, datetime.now(timezone.utc))

    assert not r.keep_item(item)


def build_reddit_feed(title: str, link: str, comments: str) -> FeedParserDict:
    feed = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<feed xmlns="http://www.w3.org/2005/Atom">',
        '<entry>',
        '<content type="html">',
    ]

    if link:
        feed.append(f'&lt;a href=&quot;{link}&quot;&gt;[link]&lt;/a&gt;')
    if comments:
        feed.append(f'&lt;a href=&quot;{comments}&quot;&gt;[comments]&lt;/a&gt;')

    feed.append('</content>')

    if link:
        feed.append(f'<link href="{link}"/>')
    if title:
        feed.append(f'<title>{title}</title>')

    feed += [
        '</content>',
        '</entry>',
        '</feed>',
    ]
    return parse('\n'.join(feed))


def test_is_reddit_media_link():
    assert is_reddit_media_link('https://i.imgur.com/w717qCT.jpg')
    assert is_reddit_media_link('https://i.redd.it/2yj5se3u8ewa1.jpg')
    assert is_reddit_media_link('https://v.redd.it/pwfzw8zs9fwa1')
    assert is_reddit_media_link('https://imgur.com/a/8Hx39hy')
    assert is_reddit_media_link('https://www.reddit.com/gallery/130ncpd')

    assert not is_reddit_media_link('https://imgurinc.com/rules')
    assert not is_reddit_media_link('https://www.reddit.com/r/greatpyrenees/comments/130qn68/mini_photo_shoot_with_my_pyr_sushi/')
