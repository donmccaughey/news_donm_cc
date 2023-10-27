import logging
import re
from pathlib import Path
from typing import AnyStr
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

log = logging.getLogger(__name__)


class URL:
    def __init__(self, url: str):
        self.__identity = None
        self.__url = url

    def __eq__(self, other: object) -> bool:
        return isinstance(other, URL) and self.__url == other.__url

    def __hash__(self) -> int:
        return hash(self.__url)

    def __lt__(self, other: 'URL') -> bool:
        return self.__url < other.__url

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.__url}')"

    def __str__(self) -> str:
        return self.__url

    @property
    def identity(self) -> str:
        if not self.__identity:
            self.__identity = url_identity(self.__url)
        return self.__identity

    def normalize(self) -> 'URL':
        cleaned = clean_url(self.__url)
        rewritten = rewrite_url(cleaned)
        return self if rewritten is self.__url else URL(rewritten)


def clean_query(query: str) -> str:
    if query:
        try:
            parameters = parse_qsl(
                query, keep_blank_values=True, strict_parsing=False,
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
    return query


def clean_url(url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    if query or fragment:
        return urlunsplit(
            (scheme, netloc, path, clean_query(query), '')
        )
    else:
        return url


def is_dirty(parameter: tuple[AnyStr, AnyStr]) -> bool:
    name, value = parameter
    return name.startswith('utm_') or name in ['leadSource', 'smid']


SOCIAL_PATH_PATTERN = re.compile(
    r'''
        /[@~][^/]+  # first path element looks like "/@username" or "/~username"
        (/.*)?      # optional trailing slash and more path elements
    ''',
    re.VERBOSE,
)


def looks_social(path: str) -> bool:
    return re.match(SOCIAL_PATH_PATTERN, path) is not None


def remove_subdomain(hostname: str, subdomains: list[str]) -> str:
    parts = hostname.split('.')
    if len(parts) > 2:
        subdomain = parts[0]
        if subdomain in subdomains:
            return '.'.join(parts[1:])
    return hostname


def rewrite_npr_url(scheme: str, path: str) -> str | None:
    parts = path.split('/')
    numbers = [
        part for part in parts
        if part.isdecimal() and len(part) > 4
    ]
    if not numbers:
        return None
    story_id = numbers[0]
    return urlunsplit((scheme, 'text.npr.org', '/' + story_id, '', ''))


def rewrite_reddit_url(scheme: str, path: str, query: str, fragment: str) -> str:
    return urlunsplit((scheme, 'old.reddit.com', path, query, fragment))


def rewrite_url(url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    match netloc:
        case 'www.npr.org':
            rewritten = rewrite_npr_url(scheme, path)
            return rewritten if rewritten else url
        case 'www.reddit.com':
            return rewrite_reddit_url(scheme, path, query, fragment)
        case _:
            return url


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


def url_identity(url: str) -> str:
    url_parts = urlsplit(url)
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
        'codeberg.org',
        'github.com',
        'gitlab.com',
        'people.kernel.org',
        'medium.com',
        'devblogs.microsoft.com',
        'twitter.com',
    ]
    if looks_social(path) or hostname in social_sites:
        return keep_path_matching(hostname, path, '/*')

    pattern_map = {
        'crates.io': '/crates/*',
        'kickstarter.com': '/projects/*',
        'sites.google.com': '/site/*',
        'npmjs.com': '/package/*',
        'pypi.org': '/project/*',
        'reddit.com': '/r/*',
    }
    if hostname in pattern_map:
        return keep_path_matching(hostname, path, pattern_map[hostname])

    return hostname