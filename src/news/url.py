class URL:
    def __init__(self, url: str):
        self.url = url

    def __eq__(self, other: 'URL') -> bool:
        return self.url == other.url

    def __hash__(self) -> int:
        return hash(self.url)

    def __lt__(self, other: 'URL') -> bool:
        return self.url < other.url

    def __repr__(self) -> str:
        return f"URL('{self.url}')"

    def __str__(self) -> str:
        return self.url
