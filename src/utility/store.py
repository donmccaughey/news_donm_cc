from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def read(self) -> str:
        pass

    @abstractmethod
    def write(self, contents: str):
        pass
