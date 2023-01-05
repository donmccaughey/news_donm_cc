import argparse
import sys

from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

from health import Health
from news import CACHE_DIR


HTML = dedent(
        '''
        <!doctype html>
        <html lang=en>
        <link rel=icon href=data:,>
        <meta charset=utf-8>
        <title>News</title>
        <p>Healthy {now}.
        '''
    ).strip()


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

    health_dir = options.cache_dir / 'health'
    health_dir.mkdir(parents=True, exist_ok=True)

    health_path = health_dir / 'index.html'

    if options.startup:
        health_path.write_text(HTML)
        sys.exit(0)

    health = Health()
    health.check()

    if health:
        html = HTML.format(now=datetime.now(timezone.utc))
        health_path.write_text(html)
    else:
        health_path.unlink(missing_ok=True)
        sys.stderr.write(health.details())

    sys.exit(health.status())


if __name__ == '__main__':
    main()
