from .store import Store


class ReadOnlyStore(Store):
    def __init__(self, store):
        self.store = store

    def __repr__(self) -> str:
        return f'ReadOnlyStore({repr(self.store)})'

    def read(self) -> str:
        return self.store.read()

    def write(self, contents: str):
        pass
