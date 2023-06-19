import logging
from datetime import datetime, timezone
from pathlib import Path

from extractor import CachedFeeds, CachedNews, parse_options
from news import LAST_EXTRACTION_FILE
from utility import iso


def main():
    options = parse_options()

    logging.basicConfig(level=logging.INFO)
    log = logging.getLogger()
    log.name = Path(__file__).name

    with CachedFeeds(options.cache_dir, options.reddit_private_rss_feed) as feeds:
        now = datetime.now(timezone.utc)
        items = []
        for feed in feeds:
            items += feed.get_items(now)
        with CachedNews(options.cache_dir, options.no_store, options.read_only) as news:
            added_count, modified_count = news.update(items, now)
            removed_count = news.remove_old(now)

    message = f'Added {added_count}, removed {removed_count} and modified {modified_count} items.'
    log.info(message)
    last_extraction_path = options.cache_dir / LAST_EXTRACTION_FILE
    last_extraction_path.write_text(f'{iso(now)} {message}\n')


if __name__ == '__main__':
    main()
