from news import URL
from .feed import Feed


class RustBlog(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'rust-lang.org',
            'rl',
            URL('https://blog.rust-lang.org/feed.xml'),
        )

    def __repr__(self) -> str:
        return 'RustBlog()'
