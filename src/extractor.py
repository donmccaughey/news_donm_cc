import argparse
import logging
import os

from datetime import datetime, timedelta, timezone
from news import Cache, DaringFireball, HackerNews, News, NoStore, ReadOnlyStore, S3Store
from pathlib import Path


def cutoff_days(arg: str) -> timedelta:
    return timedelta(days=int(arg))


def env_is_true(name: str) -> bool:
    return (
            name in os.environ
            and os.environ[name].lower() in ['true', 'yes', '1']
    )


def parse_options():
    arg_parser = argparse.ArgumentParser(description='News extractor.')
    arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                            default=Cache.DEFAULT_DIR, type=Path,
                            help='location to store cache files')
    arg_parser.add_argument('-t', '--cutoff-days', dest='cutoff_days',
                            default='30', type=cutoff_days,
                            help='discard items older than the given number of days')
    arg_parser.add_argument('--no-store', dest='no_store', default=False,
                            action='store_true', help="don't use a persistent store")
    options = arg_parser.parse_args()

    options.read_only = not env_is_true('EXTRACTOR_READ_WRITE')

    return options


def main():
    options = parse_options()

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.name = Path(__file__).name

    store = NoStore() if options.no_store else S3Store()
    if options.read_only:
        store = ReadOnlyStore(store)
    log.info(f'Using {store}')

    news_cache = Cache(options.cache_dir / Cache.NEWS_FILE)
    news = News.from_json(
        news_cache.get() or store.get() or News().to_json()
    )
    if not news_cache.is_present:
        news_cache.put(news.to_json())

    now = datetime.now(timezone.utc)

    new_count = 0
    for site in [DaringFireball(), HackerNews()]:
        new_count += news.add_new(site.get(now))

    cutoff = now - options.cutoff_days
    old_count = news.remove_old(cutoff)

    log.info(f'Added {new_count} and removed {old_count} items')

    if news.is_modified:
        json = news.to_json()
        news_cache.put(json)
        store.put(json)
        news.is_modified = False


if __name__ == '__main__':
    main()
