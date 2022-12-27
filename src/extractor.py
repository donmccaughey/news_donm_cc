import argparse
import logging
import os

from datetime import datetime, timedelta, timezone
from news import Cache, DaringFireball, HackerNews, News, NoStore, ReadOnlyStore, S3Store
from pathlib import Path
from time import sleep


def cutoff_days(arg: str) -> timedelta:
    return timedelta(days=int(arg))


def env_is_true(name: str) -> bool:
    return (
            name in os.environ
            and os.environ[name].lower() in ['true', 'yes', '1']
    )


def parse_options():
    arg_parser = argparse.ArgumentParser(description='News extractor.')
    arg_parser.add_argument('-c', '--cache-path', dest='cache_path',
                            default='./news.json', type=Path,
                            help='location to store news items')
    arg_parser.add_argument('-t', '--cutoff-days', dest='cutoff_days',
                            default='30', type=cutoff_days,
                            help='discard items older than the given number of days')
    arg_parser.add_argument('-p', '--poll', dest='poll', default=0, type=int,
                            help='minutes to sleep before checking for new items')
    arg_parser.add_argument('--no-store', dest='no_store', default=False,
                            action='store_true', help="don't use a persistent store")
    options = arg_parser.parse_args()

    options.poll_seconds = options.poll * 60
    options.read_only = not env_is_true('EXTRACTOR_READ_WRITE')

    return options


def main():
    options = parse_options()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.name = Path(__file__).name

    store = NoStore() if options.no_store else S3Store()
    if options.read_only:
        store = ReadOnlyStore(store)
    logger.info(f'Using {store}')

    cache = Cache(options.cache_path)

    news = News.from_json(
        cache.get() or store.get() or News().to_json()
    )
    if not cache.is_present:
        cache.put(news.to_json())

    sites = [DaringFireball(), HackerNews()]

    while True:
        now = datetime.now(timezone.utc)
        new_count = 0
        for site in sites:
            new_count += news.add_new(site.get(now))

        cutoff = now - options.cutoff_days
        old_count = news.remove_old(cutoff)

        logger.info(f'Added {new_count} and removed {old_count} items')

        if news.is_modified:
            json = news.to_json()
            cache.put(json)
            store.put(json)
            news.is_modified = False

        if options.poll:
            sleep(options.poll_seconds)
        else:
            break


if __name__ == '__main__':
    main()
