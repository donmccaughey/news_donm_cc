from abc import ABC, abstractmethod
from serialize.jsontype import JSONDict, JSONList


class Encodable(ABC):
    @staticmethod
    @abstractmethod
    def decode(encoded: JSONDict | JSONList) -> 'Encodable':
        pass

    @abstractmethod
    def encode(self) -> JSONDict | JSONList:
        pass
