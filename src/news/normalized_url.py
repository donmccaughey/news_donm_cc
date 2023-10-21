from .url import URL, clean_url, rewrite_url


class NormalizedURL(URL):
    def __init__(self, url: str):
        cleaned = clean_url(url)
        rewritten = rewrite_url(cleaned)
        super().__init__(rewritten)
