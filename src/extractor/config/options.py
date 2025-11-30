from argparse import Namespace, ArgumentParser
from pathlib import Path

from news import CACHE_DIR


def parse_options() -> Namespace:
    arg_parser = ArgumentParser(description='News extractor.')
    arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                            default=CACHE_DIR, type=Path,
                            help='location to store cache files')
    arg_parser.add_argument('--no-store', dest='no_store', default=False,
                            action='store_true', help="don't use a persistent store")
    return arg_parser.parse_args()
