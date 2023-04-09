import logging
from pathlib import Path
from typing import AnyStr
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

log = logging.getLogger(__name__)


class URL:
    def __init__(self, url: str):
        self.url = url

    def __eq__(self, other: 'URL') -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __lt__(self, other: 'URL') -> bool:
        return self.url < other.url

    def __repr__(self) -> str:
        return f"URL('{self.url}')"

    def __str__(self) -> str:
        return self.url

    def clean(self) -> 'URL':
        scheme, netloc, path, query, fragment = urlsplit(self.url)
        if query or fragment:
            return URL(
                urlunsplit(
                    (scheme, netloc, path, clean_query(query), '')
                )
            )
        else:
            return self

    @property
    def identity(self) -> str:
        url_parts = urlsplit(self.url)
        hostname = url_parts.hostname
        path = url_parts.path

        unimportant_subdomains = [
            'blog', 'blogs', 'community', 'docs', 'en', 'web', 'www', 'www2'
        ]
        hostname = remove_subdomain(hostname, unimportant_subdomains)

        hostname_map = {
            'lite.cnn.com': 'cnn.com',
            'gist.github.com': 'github.com',
            'text.npr.org': 'npr.org',
            'old.reddit.com': 'reddit.com',
        }
        if hostname in hostname_map:
            hostname = hostname_map[hostname]

        social_sites = [
            'github.com',
            'gitlab.com',
            'people.kernel.org',
            'medium.com',
            'devblogs.microsoft.com',
            'sr.ht',
            'twitter.com',
        ]
        if looks_social(hostname, path) or hostname in social_sites:
            return keep_path_matching(hostname, path, '/*')

        pattern_map = {
            'crates.io': '/crates/*',
            'sites.google.com': '/site/*',
            'npmjs.com': '/package/*',
            'pypi.org': '/project/*',
            'reddit.com': '/r/*',
        }
        if hostname in pattern_map:
            return keep_path_matching(hostname, path, pattern_map[hostname])

        return hostname


def clean_query(query: str) -> str:
    if query:
        try:
            parameters = parse_qsl(
                query, keep_blank_values=True, strict_parsing=True,
                encoding='utf-8', errors='strict'
            )
            clean_parameters = [
                parameter for parameter in parameters
                if not is_dirty(parameter)
            ]
            if len(parameters) != len(clean_parameters):
                return urlencode(
                    list(clean_parameters), encoding='utf-8', errors='strict'
                )
        except UnicodeError as e:
            log.warning(f'Unicode Error parsing "{query}": {e}')
        except ValueError as e:
            log.warning(f'Value Error parsing "{query}": {e}')
    return query


def is_dirty(parameter: tuple[AnyStr, AnyStr]) -> bool:
    name, value = parameter
    return name.startswith('utm_')


def looks_social(hostname: str, path: str) -> bool:
    subdomains = hostname.split('.')
    return (
        'social' in subdomains
        and path.startswith('/@')
        and len(path) > 2
    )


def remove_subdomain(hostname: str, subdomains: list[str]) -> str:
    parts = hostname.split('.')
    if len(parts) > 2:
        subdomain = parts[0]
        if subdomain in subdomains:
            return '.'.join(parts[1:])
    return hostname


def keep_path_matching(hostname: str, path: str, pattern: str) -> str:
    parts = Path(path).parts
    patterns = Path(pattern).parts
    if len(parts) < len(patterns):
        return hostname

    matching = []
    for part, pattern in zip(parts, patterns):
        match pattern:
            case '/':
                matching.append('')
            case '*':
                matching.append(part)
            case _:
                if part == pattern:
                    matching.append(part)
                else:
                    return hostname

    return hostname + '/'.join(matching)
