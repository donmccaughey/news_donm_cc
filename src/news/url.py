class URL:
    def __init__(self, url: str):
        self.url = url

    def __eq__(self, other: 'URL'):
        return self.url == other.url

    def __hash__(self):
        return hash(self.url)

    def __repr__(self) -> str:
        return f'URL<{self.url}>'

    def __str__(self) -> str:
        return self.url
