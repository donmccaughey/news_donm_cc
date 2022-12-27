import argparse

from news import Cache, News, S3Store
from pathlib import Path


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Query news.')
    arg_parser.add_argument('-c', '--cache-path', dest='cache_path',
                            default='./news.json', type=Path,
                            help='location to store news items')
    arg_parser.add_argument('--no-store', dest='no_store', default=False,
                            action='store_true', help="don't use a persistent store")
    return arg_parser.parse_args()


def main():
    options = parse_options()

    if options.no_store:
        json = Cache(options.cache_path).get()
    else:
        json = S3Store().get()

    news = News.from_json(json)

    urls = [item.url for item in news]
    urls.sort()
    for url in urls:
        print(url)


if __name__ == '__main__':
    main()
