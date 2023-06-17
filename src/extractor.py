import logging
import os
from argparse import ArgumentParser, Namespace
from datetime import datetime, timezone
from pathlib import Path

from feeds import Feeds
from news import CACHE_DIR, LAST_EXTRACTION_FILE, News, NEWS_FILE, NoStore, ReadOnlyStore, S3Store
from utility import Cache, iso


class CachedFeeds:
    def __init__(self, options: Namespace):
        self.cache = Cache(options.cache_dir / 'feeds.json')
        self.feeds = Feeds.from_json(
            self.cache.get() or Feeds().to_json(),
            vars(options),
        )

    def __enter__(self) -> Feeds:
        return self.feeds

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cache.put(self.feeds.to_json())


class CachedNews:
    def __init__(self, options: Namespace):
        self.store = NoStore() if options.no_store else S3Store()
        if options.read_only:
            self.store = ReadOnlyStore(self.store)

        self.cache = Cache(options.cache_dir / NEWS_FILE)

        self.news = News.from_json(
            self.cache.get() or self.store.get() or News().to_json()
        )

    def __enter__(self) -> News:
        return self.news

    def __exit__(self, exc_type, exc_val, exc_tb):
        json = self.news.to_json()
        self.cache.put(json)
        self.store.put(json)


def env_is_true(name: str) -> bool:
    return (
        name in os.environ
        and os.environ[name].lower() in ['true', 'yes', '1']
    )


def parse_options() -> Namespace:
    arg_parser = ArgumentParser(description='News extractor.')
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

    with CachedFeeds(options) as feeds:
        now = datetime.now(timezone.utc)
        items = []
        for feed in feeds:
            items += feed.get_items(now)
        with CachedNews(options) as news:
            added_count, modified_count = news.update(items, now)
            removed_count = news.remove_old(now)

    message = f'Added {added_count}, removed {removed_count} and modified {modified_count} items.'
    log.info(message)
    last_extraction_path = options.cache_dir / LAST_EXTRACTION_FILE
    last_extraction_path.write_text(f'{iso(now)} {message}\n')


if __name__ == '__main__':
    main()
