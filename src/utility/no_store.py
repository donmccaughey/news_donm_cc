from utility.store import Store


class NoStore(Store):
    def __repr__(self) -> str:
        return 'NoStore()'

    def read(self) -> str:
        return ''

    def write(self, contents: str):
        pass
