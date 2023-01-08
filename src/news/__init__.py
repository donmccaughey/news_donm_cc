from .item import Item
from .news import News
from .source import Source
from .store import NoStore, ReadOnlyStore, S3Store
from .url import URL

CACHE_DIR = '/var/lib/news'
NEWS_FILE = 'news.json'
LAST_EXTRACTION_FILE = 'last-extraction.txt'
