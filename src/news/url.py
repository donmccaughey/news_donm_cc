from pathlib import Path
from urllib.parse import urlsplit


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

    @property
    def identity(self) -> str:
        url_parts = urlsplit(self.url)
        hostname = url_parts.hostname
        path = url_parts.path

        hostname = clip_subdomains(hostname, [
            'blog', 'blogs', 'community', 'docs', 'en', 'www'
        ])

        if hostname == 'old.reddit.com':
            hostname = 'reddit.com'

        if hostname == 'github.com':
            return keep_path_matching(hostname, path, '/*')

        if hostname == 'reddit.com':
            return keep_path_matching(hostname, path, '/r/*')

        if hostname == 'twitter.com':
            return keep_path_matching(hostname, path, '/*')

        return hostname


def clip_subdomains(hostname: str, subdomains: list[str]) -> str:
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
