import argparse
import sys

from datetime import datetime, timezone
from pathlib import Path

from health import Health
from news import CACHE_DIR


def parse_options():
    arg_parser = argparse.ArgumentParser(description='News health check.')
    arg_parser.add_argument('-c', '--cache-dir', dest='cache_dir',
                            default=CACHE_DIR, type=Path,
                            help='location to write the health file')
    arg_parser.add_argument('--startup', dest='startup',
                            default=False, action='store_true',
                            help='write the health file and exit')
    options = arg_parser.parse_args()
    return options


def main():
    options = parse_options()

    health = Health()
    if not options.startup:
        health.check()

    health_path = options.cache_dir / 'healthy.txt'
    if health:
        now = datetime.now(timezone.utc)
        health_path.write_text(f'healthy {now}\n')
    else:
        health_path.unlink(missing_ok=True)
        sys.stderr.write(health.details())

    sys.exit(health.status())


if __name__ == '__main__':
    main()
