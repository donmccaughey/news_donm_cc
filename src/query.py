import argparse
from collections import defaultdict
from pathlib import Path

from news import Item, News
from extractor import S3Store
from utility import CachedFile


def parse_options() -> argparse.Namespace:
    arg_parser = argparse.ArgumentParser(description='Query news.')
    arg_parser.add_argument('-o', '--open', dest='news_path', type=Path,
                            help='location of news items JSON')
    arg_parser.add_argument('--site-id', dest='site_ids',
                            type=str, action='append',
                            help='site ID to include in results ("df", "hn", "lob", ...)')

    query_choices = ['terms', 'terms-by-frequency', 'urls', 'urls-by-site', 'urls-by-source-counts']
    arg_parser.add_argument('query', metavar='QUERY',
                            choices=query_choices, default='urls',
                            help=str(query_choices))

    return arg_parser.parse_args()


def query_terms(news: News):
    index = news.index
    term_width = 0
    for term in index.terms.keys():
        term_width = max(term_width, len(term))
    for term in sorted(index.terms.keys()):
        print(f'{term:<{term_width}} {len(index.terms[term]):>4}')
    print('')
    print(f'{len(index.terms)} terms')


def query_terms_by_frequency(news: News):
    index = news.index
    term_width = 0
    for term in index.terms.keys():
        term_width = max(term_width, len(term))
    sorted_terms = sorted(index.terms.items(), key=lambda item: (-len(item[1]), item[0]))
    for term, indices in sorted_terms:
        print(f'{term:<{term_width}} {len(indices):>4}')
    print('')
    print(f'{len(index.terms)} terms')


def query_urls(news: News):
    urls = [item.url for item in news]
    urls.sort()
    for url in urls:
        print(url)


def query_urls_by_site(news: News):
    urls = [item.url for item in news]
    groups = defaultdict(list)
    for url in urls:
        groups[url.identity].append(url)
    items = list(groups.items())
    items.sort(key=lambda item: (-len(item[1]), item[0]))
    for identity, urls in items:
        print(identity, len(urls))
        for url in urls:
            print('    ', url)


def query_urls_by_source_counts(news: News):
    by_count = list(news)
    by_count.sort(key=lambda item: (-item.count, item.sources[0].site_id, item.title))
    w1 = w2 = 0
    for item in by_count:
        w1 = max(w1, len(item.sources[0].site_id))
        w2 = max(w2, len(item.url.identity))
    for item in by_count:
        print(f'{item.count:4}\t{item.sources[0].site_id:{w1}}\t{item.url.identity:{w2}}\t{item.title}')


def main():
    options = parse_options()

    if options.news_path:
        json = CachedFile(options.news_path).read()
    else:
        json = S3Store().read()

    news = News.from_json(json)

    if options.site_ids:
        def from_site(item: Item):
            for source in item.sources:
                if source.site_id in options.site_ids:
                    return True
            return False

        news = News(items=list(filter(from_site, news)))

    match options.query:
        case 'terms':
            query_terms(news)
        case 'terms-by-frequency':
            query_terms_by_frequency(news)
        case 'urls':
            query_urls(news)
        case 'urls-by-site':
            query_urls_by_site(news)
        case 'urls-by-source-counts':
            query_urls_by_source_counts(news)


if __name__ == '__main__':
    main()
