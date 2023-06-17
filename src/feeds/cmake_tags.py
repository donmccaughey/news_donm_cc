from news import URL
from .feed import Feed


class CMakeTags(Feed):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://gitlab.kitware.com/cmake/cmake/-/tags?format=atom'),
            'CMake Tags', 'cm',
        )

    def __repr__(self) -> str:
        return 'CMakeTags()'
