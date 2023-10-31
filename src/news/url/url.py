import logging
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from .identity import url_identity
from .rewrite import rewrite_url


log = logging.getLogger(__name__)


class URL:
    def __init__(self, url: str):
        self.__identity: str | None = None
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


def is_dirty(parameter: tuple[str, str]) -> bool:
    name, value = parameter
    return name.startswith('utm_') or name in ['leadSource', 'smid']
