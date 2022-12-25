from .url import URL


class Source:
    def __init__(self, url: URL, site_id: str):
        self.url = url
        self.site_id = site_id

    def __repr__(self) -> str:
        return f"Source({repr(self.url)}, '{self.site_id}')"

    @staticmethod
    def decode(encoded: dict[str, str] | str) -> 'Source':
        match encoded:
            case dict():
                return Source(URL(encoded['url']), encoded['site_id'])
            case str():
                return Source(URL(encoded), 'hn')
            case _:
                raise RuntimeError(repr(encoded))

    def encode(self) -> dict[str, str]:
        return {
            'url': str(self.url),
            'site_id': self.site_id,
        }
