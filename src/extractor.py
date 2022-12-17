from datetime import datetime, timedelta, timezone
from news import Cache, Items, Source, Store, URL
from pathlib import Path


cache_file = 'news.json'
cutoff_days = 30
sources = [
    Source(URL('https://news.ycombinator.com/rss')),
]


def main():
    cache_path = Path.cwd() / cache_file
    now = datetime.now(timezone.utc)

    cache = Cache(cache_path)
    store = Store()

    items = Items.from_json(
        cache.get() or store.get() or Items().to_json()
    )

    for source in sources:
        items += source.get(now)

    cutoff = now - timedelta(days=cutoff_days)
    items.prune(cutoff)

    json = items.to_json()
    cache.put(json)
    store.put(json)


if __name__ == '__main__':
    main()
