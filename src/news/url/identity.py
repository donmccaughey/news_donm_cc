import re
from pathlib import Path
from urllib.parse import urlsplit


HOSTNAME_MAP = {
    'lite.cnn.com': 'cnn.com',
    'gist.github.com': 'github.com',
    'text.npr.org': 'npr.org',
    'old.reddit.com': 'reddit.com',
}


IDENTITY_PATTERNS = {
    'crates.io': '/crates/*',
    'kickstarter.com': '/projects/*',
    'sites.google.com': '/site/*',
    'npmjs.com': '/package/*',
    'pypi.org': '/project/*',
    'reddit.com': '/r/*',
}


SOCIAL_PATH_PATTERN = re.compile(
    r'''
        /[@~][^/]+  # first path element looks like "/@username" or "/~username"
        (/.*)?      # optional trailing slash and more path elements
    ''',
    re.VERBOSE,
)


SOCIAL_SITES = {
    'codeberg.org',
    'github.com',
    'gitlab.com',
    'people.kernel.org',
    'medium.com',
    'devblogs.microsoft.com',
    'twitter.com',
}


UNIMPORTANT_SUBDOMAINS = {
    'blog',
    'blogs',
    'community',
    'docs',
    'en',
    'newsletter',
    'web',
    'www',
    'www2'
}


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


def looks_social(path: str) -> bool:
    return re.match(SOCIAL_PATH_PATTERN, path) is not None


def remove_subdomain(hostname: str, subdomains: set[str]) -> str:
    parts = hostname.split('.')
    if len(parts) > 2:
        subdomain = parts[0]
        if subdomain in subdomains:
            return '.'.join(parts[1:])
    return hostname


def url_identity(url: str) -> str:
    url_parts = urlsplit(url)
    hostname = url_parts.hostname or ''
    path = url_parts.path

    hostname = remove_subdomain(hostname, UNIMPORTANT_SUBDOMAINS)

    if hostname in HOSTNAME_MAP:
        hostname = HOSTNAME_MAP[hostname]

    if looks_social(path) or (hostname in SOCIAL_SITES):
        return keep_path_matching(hostname, path, '/*')

    if hostname in IDENTITY_PATTERNS:
        return keep_path_matching(hostname, path, IDENTITY_PATTERNS[hostname])

    return hostname
