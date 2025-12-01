from __future__ import annotations

import sys

from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path

from news import CACHE_DIR


@dataclass(frozen=True, slots=True)
class Options:
    cache_dir: Path
    no_store: bool

    @classmethod
    def parse(cls, args: list[str] | None = None) -> Options:
        arg_parser = ArgumentParser(description='News extractor.')
        arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                                default=CACHE_DIR, type=Path,
                                help='location to store cache files')
        arg_parser.add_argument('--no-store', dest='no_store', default=False,
                                action='store_true',
                                help="don't use a persistent store")

        if args is None:
            args = sys.argv[1:]
        namespace = arg_parser.parse_args(args)

        return cls(
            cache_dir=namespace.cache_dir,
            no_store=namespace.no_store,
        )
