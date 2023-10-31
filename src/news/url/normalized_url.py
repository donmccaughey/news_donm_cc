from .clean import clean_url
from .rewrite import rewrite_url
from .url import URL


class NormalizedURL(URL):
    def __init__(self, url: str):
        cleaned = clean_url(url)
        rewritten = rewrite_url(cleaned)
        super().__init__(rewritten)
