from news import URL
from .feed import Feed


class CMakeTags(Feed):
    def __init__(self):
        super().__init__(
            'CMake Tags',
            'cm',
            URL('https://gitlab.kitware.com/cmake/cmake/-/tags?format=atom')
        )

    def __repr__(self) -> str:
        return 'CMakeTags()'
