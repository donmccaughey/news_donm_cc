from news import URL
from .feed import Feed


class RustBlog(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            URL('https://blog.rust-lang.org/feed.xml'),
            'rust-lang.org',
            'rl',
        )

    def __repr__(self) -> str:
        return 'RustBlog()'
