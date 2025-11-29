import os
from argparse import Namespace, ArgumentParser
from pathlib import Path

from news import CACHE_DIR


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
