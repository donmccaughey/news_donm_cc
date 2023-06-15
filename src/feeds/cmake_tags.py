from news import URL
from .site import Site


class CMakeTags(Site):
    def __init__(self, _options: dict):
        super().__init__(
            URL('https://gitlab.kitware.com/cmake/cmake/-/tags?format=atom'),
            'CMake Tags', 'cm',
        )

    def __repr__(self) -> str:
        return 'CMakeTags()'
