import argparse
import sys
from typing import cast

import bs4
import requests
from bs4 import Tag


def parse_options():
    arg_parser = argparse.ArgumentParser(description='Find YouTube user.')
    arg_parser.add_argument('url', metavar='URL', help='YouTube URL')
    return arg_parser.parse_args()


def find_youtube_user_url(html_text: str) -> str | None:
    soup = bs4.BeautifulSoup(html_text, 'html.parser')
    author = soup.find(itemtype='http://schema.org/Person')
    if isinstance(author, Tag):
        link = author.find(itemprop='url')
        if isinstance(link, Tag):
            return cast(str | None, link['href'])
    return None


def main():
    options = parse_options()
    response = requests.get(options.url)
    if response.status_code == 200:
        url = find_youtube_user_url(response.text)
        if url:
            print(url)
        else:
            print(f'User not found for {options.url}')
    else:
        print(f'Error {response.status_code}: {response.reason} getting {options.url}')
        sys.exit(1)


if __name__ == '__main__':
    main()
