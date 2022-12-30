from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


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
        parts = urlsplit(self.url)
        if parts.query or parts.fragment:
            cleaned = urlunsplit(
                (parts.scheme, parts.netloc, parts.path, '', '')
            )
            return URL(cleaned)
        else:
            return self

    @property
    def identity(self) -> str:
        url_parts = urlsplit(self.url)
        hostname = url_parts.hostname
        path = url_parts.path

        subdomains = ['blog', 'blogs', 'community', 'docs', 'en', 'www']
        hostname = remove_subdomain(hostname, subdomains)

        hostname_map = {
            'lite.cnn.com': 'cnn.com',
            'text.npr.org': 'npr.org',
            'old.reddit.com': 'reddit.com',
        }
        if hostname in hostname_map:
            hostname = hostname_map[hostname]

        path_map = {
            'github.com': '/*',
            'devblogs.microsoft.com': '/*',
            'reddit.com': '/r/*',
            'twitter.com': '/*',
        }
        if hostname in path_map:
            return keep_path_matching(hostname, path, path_map[hostname])

        return hostname


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
