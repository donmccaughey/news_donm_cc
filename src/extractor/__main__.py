import logging

from datetime import datetime, timezone
from pathlib import Path

from extractor import CachedFeeds, CachedNews, Config, Environ, Options
from extractor import S3Creds, S3Store
from news import LAST_EXTRACTION_FILE
from utility import iso, NoStore, ReadOnlyStore, Store


options = Options.parse()
environ = Environ.read()
aws_s3_creds = S3Creds.for_aws()
config = Config.build(options, environ, aws_s3_creds)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()
log.name = Path(__file__).name

store: Store
if config.no_store:
    store = NoStore()
else:
    store = S3Store(config.s3_creds)

if config.read_only:
    store = ReadOnlyStore(store)

with CachedFeeds(config.cache_dir, config.reddit_private_rss_feed) as feeds:
    now = datetime.now(timezone.utc)
    items = []
    for feed in feeds:
        items += feed.get_items(now)
    with CachedNews(config.cache_dir, store) as news:
        added_count, modified_count = news.update(items, now)
        removed_count = news.remove_old(now)

message = f'Added {added_count}, removed {removed_count} and modified {modified_count} items.'
log.info(message)
last_extraction_path = config.cache_dir / LAST_EXTRACTION_FILE
last_extraction_path.write_text(f'{iso(now)} {message}\n')
