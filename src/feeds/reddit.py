import logging
from datetime import datetime
from typing import Tuple
from urllib.parse import urlsplit

import bs4
from .skip_sites import SKIP_SITES
from .feed import Feed
from news import Item, Source, URL

log = logging.getLogger(__name__)


class Reddit(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'Reddit',
            'r',
            URL(options['reddit_private_rss_feed']),
        )

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

        url, source = extract_links(content, default=URL(entry.link))

        identity_parts = source.identity.split('/')
        site_id = '/'.join(identity_parts[1:])

        return Item(
            url=url,
            title=entry.title,
            sources=[Source(source, site_id)],
            created=now,
            modified=now,
        )


def extract_links(content, default: URL | None = None) -> Tuple[URL, URL]:
    link, comments = default, default
    soup = bs4.BeautifulSoup(content, 'html.parser')
    for anchor in soup.find_all('a'):
        if anchor.text.strip() == '[link]':
            href = anchor['href']
            if not is_reddit_media_link(href):
                link = URL(href).clean()
        elif anchor.text.strip() == '[comments]':
            comments = URL(anchor['href'])
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
