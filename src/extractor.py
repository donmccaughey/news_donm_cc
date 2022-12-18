import argparse

from datetime import datetime, timedelta, timezone
from news import Cache, Items, Source, Store, URL
from pathlib import Path
from time import sleep


sources = [
    Source(URL('https://news.ycombinator.com/rss')),
]


def cutoff_days(arg: str) -> timedelta:
    return timedelta(days=int(arg))


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
    options = arg_parser.parse_args()
    options.poll_seconds = options.poll * 60
    return options


def main():
    options = parse_options()

    cache = Cache(options.cache_path)
    store = Store()

    items = Items.from_json(
        cache.get() or store.get() or Items().to_json()
    )

    while True:
        now = datetime.now(timezone.utc)
        cutoff = now - options.cutoff_days

        for source in sources:
            items += source.get(now)

        items.prune(cutoff)

        json = items.to_json()
        cache.put(json)
        store.put(json)

        if options.poll:
            sleep(options.poll_seconds)
        else:
            break


if __name__ == '__main__':
    main()
