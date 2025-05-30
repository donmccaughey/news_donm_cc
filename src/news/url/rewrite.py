from urllib.parse import urlsplit, urlunsplit


# See https://www.reddit.com/r/TheoryOfReddit/comments/10ugn9j/i_just_learned_about_the_reddit_web_ui/
REDDIT_NETLOCS = {
    'i.reddit.com',
    'm.reddit.com',
    'sh.reddit.com',
    'www.reddit.com',
}


def rewrite_medium_url(url: str) -> str:
    return 'https://freedium.cfd/' + url


def is_npr_story_id(part: str) -> bool:
    if part.isdecimal() and len(part) > 4:
        return True
    if part.startswith('g-s1-') and part[5:].isdecimal():
        return True
    if part.startswith('nx-s1-') and part[6:].isdecimal():
        return True
    return False


def rewrite_npr_url(scheme: str, path: str) -> str | None:
    parts = path.split('/')
    story_id_parts = [part for part in parts if is_npr_story_id(part)]
    if not story_id_parts:
        return None
    story_id = story_id_parts[0]
    return urlunsplit((scheme, 'text.npr.org', '/' + story_id, '', ''))


def rewrite_reddit_url(scheme: str, path: str, query: str, fragment: str) -> str:
    return urlunsplit((scheme, 'old.reddit.com', path, query, fragment))


def rewrite_reuters_url(scheme: str, path: str) -> str:
    return urlunsplit((scheme, 'neuters.de', path, '', ''))


def rewrite_url(url: str) -> str:
    scheme, netloc, path, query, fragment = urlsplit(url)
    match netloc:
        case 'medium.com':
            return rewrite_medium_url(url)
        case 'www.npr.org':
            rewritten = rewrite_npr_url(scheme, path)
            return rewritten if rewritten else url
        case 'www.reuters.com':
            # TODO (2025-03-18): re-enable if neuters.de fixes captcha error
            # https://github.com/HookedBehemoth/neuters/issues/42
            # return rewrite_reuters_url(scheme, path)
            return url
        case _ if netloc in REDDIT_NETLOCS:
            return rewrite_reddit_url(scheme, path, query, fragment)
        case _:
            return url
