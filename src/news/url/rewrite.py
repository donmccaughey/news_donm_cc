from urllib.parse import urlsplit, urlunsplit


# See https://www.reddit.com/r/TheoryOfReddit/comments/10ugn9j/i_just_learned_about_the_reddit_web_ui/
REDDIT_NETLOCS = {
    'i.reddit.com',
    'm.reddit.com',
    'sh.reddit.com',
    'www.reddit.com',
}


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


def rewrite_reuters_url(scheme: str, path: str) -> str:
    return urlunsplit((scheme, 'neuters.de', path, '', ''))


def rewrite_url(url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    match netloc:
        case 'www.npr.org':
            rewritten = rewrite_npr_url(scheme, path)
            return rewritten if rewritten else url
        case 'www.reuters.com':
            return rewrite_reuters_url(scheme, path)
        case _ if netloc in REDDIT_NETLOCS:
            return rewrite_reddit_url(scheme, path, query, fragment)
        case _:
            return url
