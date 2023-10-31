from urllib.parse import urlsplit, urlunsplit


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
