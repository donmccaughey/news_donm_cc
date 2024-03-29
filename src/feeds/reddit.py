import logging
from datetime import datetime
from typing import Tuple
from urllib.parse import urlsplit

import bs4
from .skip_sites import SKIP_SITES
from .feed import Feed
from news import Item, Source
from news.url import NormalizedURL, URL


log = logging.getLogger(__name__)


class Reddit(Feed):
    def __init__(self, url: URL):
        super().__init__('Reddit', 'r', url)

    def __repr__(self) -> str:
        return 'Reddit()'

    def keep_item(self, item: Item) -> bool:
        return item.url.identity not in SKIP_SITES

    def parse_entry(self, entry, now: datetime) -> Item:
        if len(entry.content):
            content = entry.content[0].value
        else:
            content = ''
            log.warning(f'No content for "{entry.title}" (entry.link)')

        url, source = extract_links(content, default=NormalizedURL(entry.link))

        identity_parts = source.identity.split('/')
        site_id = '/'.join(identity_parts[1:])

        return Item(
            url=url,
            title=entry.title,
            sources=[Source(source, site_id)],
            created=now,
            modified=now,
        )


def extract_links(
        content, *, default: NormalizedURL
) -> Tuple[NormalizedURL, NormalizedURL]:
    link, comments = default, default
    soup = bs4.BeautifulSoup(content, 'html.parser')
    for anchor in soup.find_all('a'):
        if anchor.text.strip() == '[link]':
            href = anchor['href']
            if not is_reddit_media_link(href):
                href = make_reddit_absolute(href)
                link = NormalizedURL(href)
        elif anchor.text.strip() == '[comments]':
            comments = NormalizedURL(anchor['href'])
    return link, comments


def is_reddit_media_link(link: str) -> bool:
    scheme, netloc, path, query, fragment = urlsplit(link)
    if netloc in ['i.imgur.com', 'i.redd.it', 'v.redd.it']:
        return True
    if netloc == 'imgur.com' and path.startswith('/a/'):
        return True
    if netloc == 'www.reddit.com' and path.startswith('/gallery/'):
        return True
    return False


def make_reddit_absolute(href: str) -> str:
    if href.startswith('/r/u_'):
        return 'https://www.reddit.com/user/' + href[5:]
    elif href.startswith('/r/'):
        return 'https://www.reddit.com' + href
    else:
        return href
