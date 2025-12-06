import argparse

from pathlib import Path

from news import CACHE_DIR


def parse_options():
    arg_parser = argparse.ArgumentParser(description='News health check.')
    arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                            default=CACHE_DIR, type=Path,
                            help='location to write the health file')
    arg_parser.add_argument('--startup', dest='startup',
                            default=False, action='store_true',
                            help='write the health file without checking and exit')
    options = arg_parser.parse_args()
    return options
