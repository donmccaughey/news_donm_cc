from utility.jsontype import JSONDict
from .url import URL


class Source:
    def __init__(self, url: URL, site_id: str):
        self.url = url.clean().rewrite()
        self.site_id = site_id

    def __eq__(self, other: 'Source') -> bool:
        return (
            isinstance(other, Source)
            and self.site_id == other.site_id
            and self.url == other.url
        )

    def __hash__(self) -> int:
        return hash((self.url, self.site_id))

    def __repr__(self) -> str:
        return f"Source({repr(self.url)}, '{self.site_id}')"

    @staticmethod
    def decode(encoded: JSONDict) -> 'Source':
        return Source(
            url=URL(encoded['url']),
            site_id=encoded['site_id'],
        )

    def encode(self) -> JSONDict:
        return {
            'url': str(self.url),
            'site_id': self.site_id,
        }
