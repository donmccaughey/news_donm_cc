from typing import cast

from jsontype import JSONDict, JSONList
from serialize import Encodable
from .url import NormalizedURL


class Source(Encodable):
    def __init__(self, url: NormalizedURL, site_id: str, count: int = 1):
        self.url = url
        self.site_id = site_id
        self.count = count

    def __eq__(self, other: object) -> bool:
        return (
            isinstance(other, Source)
            and self.site_id == other.site_id
            and self.url == other.url
        )

    def __hash__(self) -> int:
        return hash((self.url, self.site_id))

    def __lt__(self, other: 'Source') -> bool:
        return self.site_id < other.site_id

    def __repr__(self) -> str:
        return f"Source({repr(self.url)}, '{self.site_id}', {self.count})"

    def update_from(self, other: 'Source'):
        self.count += other.count

    @staticmethod
    def decode(encoded: JSONDict | JSONList) -> 'Source':
        encoded = cast(JSONDict, encoded)
        return Source(
            url=NormalizedURL(cast(str, encoded['url'])),
            site_id=cast(str, encoded['site_id']),
            count=cast(int, encoded.get('count', 1))
        )

    def encode(self) -> JSONDict:
        return {
            'url': str(self.url),
            'site_id': self.site_id,
            'count': self.count,
        }
