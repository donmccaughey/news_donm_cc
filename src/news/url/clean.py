import logging
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


log = logging.getLogger(__name__)


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
