import argparse
from collections import defaultdict
from pathlib import Path

from news import News
from extractor import S3Store
from utility import Cache


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Query news.')
    arg_parser.add_argument('-o', '--open', dest='news_path', type=Path,
                            help='location of news items JSON')

    query_choices = ['urls', 'urls-by-site', 'urls-by-source-counts']
    arg_parser.add_argument('query', metavar='QUERY',
                            choices=query_choices, default='urls',
                            help=str(query_choices))

    return arg_parser.parse_args()


def query_urls(news):
    urls = [item.url for item in news]
    urls.sort()
    for url in urls:
        print(url)


def query_urls_by_site(news):
    urls = [item.url for item in news]
    groups = defaultdict(list)
    for url in urls:
        groups[url.identity].append(url)
    groups = list(groups.items())
    groups.sort(key=lambda item: (-len(item[1]), item[0]))
    for identity, urls in groups:
        print(identity, len(urls))
        for url in urls:
            print('    ', url)


def query_urls_by_source_counts(news):
    by_count = [(item.count, item.url) for item in news]
    by_count.sort(key=lambda t: (-t[0], str(t[1])))
    for count, url in by_count:
        print(f'{count}: {url}')


def main():
    options = parse_options()

    if options.news_path:
        json = Cache(options.news_path).get()
    else:
        json = S3Store().get()

    news = News.from_json(json)

    match options.query:
        case 'urls':
            query_urls(news)
        case 'urls-by-site':
            query_urls_by_site(news)
        case 'urls-by-source-counts':
            query_urls_by_source_counts(news)


if __name__ == '__main__':
    main()
