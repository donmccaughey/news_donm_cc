from news import URL
from .feed import Feed


class CMakeTags(Feed):
    def __init__(self, options: dict):
        super().__init__(
            options,
            'CMake Tags',
            'cm',
            URL('https://gitlab.kitware.com/cmake/cmake/-/tags?format=atom')
        )

    def __repr__(self) -> str:
        return 'CMakeTags()'
