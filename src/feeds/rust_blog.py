from news import URL
from .site import Site


class RustBlog(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://blog.rust-lang.org/feed.xml'),
            'rust-lang.org', 'rl',
        )

    def __repr__(self) -> str:
        return 'RustBlog()'
