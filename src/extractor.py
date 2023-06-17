import argparse
import logging
import os
from datetime import datetime, timezone
from pathlib import Path

from feeds import Feeds
from news import CACHE_DIR, LAST_EXTRACTION_FILE, News, NEWS_FILE, NoStore, ReadOnlyStore, S3Store
from utility import Cache, iso


def env_is_true(name: str) -> bool:
    return (
        name in os.environ
        and os.environ[name].lower() in ['true', 'yes', '1']
    )


def parse_options():
    arg_parser = argparse.ArgumentParser(description='News extractor.')
    arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                            default=CACHE_DIR, type=Path,
                            help='location to store cache files')
    arg_parser.add_argument('--no-store', dest='no_store', default=False,
                            action='store_true', help="don't use a persistent store")
    options = arg_parser.parse_args()

    options.read_only = not env_is_true('EXTRACTOR_READ_WRITE')
    options.reddit_private_rss_feed = os.environ['REDDIT_PRIVATE_RSS_FEED']

    return options


def main():
    options = parse_options()

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.name = Path(__file__).name

    feeds_cache = Cache(options.cache_dir / 'feeds.json')
    feeds = Feeds.from_json(feeds_cache.get(), vars(options))

    store = NoStore() if options.no_store else S3Store()
    if options.read_only:
        store = ReadOnlyStore(store)

    news_cache = Cache(options.cache_dir / NEWS_FILE)
    news = News.from_json(
        news_cache.get() or store.get() or News().to_json()
    )

    now = datetime.now(timezone.utc)
    new_total, modified_total = 0, 0
    for feed in feeds:
        new_count, modified_count = news.update(feed.get_items(now), now)
        new_total += new_count
        modified_total += modified_count

    old_total = news.remove_old(now)

    json = news.to_json()
    news_cache.put(json)
    store.put(json)

    feeds_cache.put(feeds.to_json())

    message = f'Added {new_total}, removed {old_total} and modified {modified_total} items.'

    log.info(message)
    last_extraction_path = options.cache_dir / LAST_EXTRACTION_FILE
    last_extraction_path.write_text(f'{iso(now)} {message}\n')


if __name__ == '__main__':
    main()
