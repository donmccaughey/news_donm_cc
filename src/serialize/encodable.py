from abc import ABC, abstractmethod
from jsontype import JSONArray, JSONObject


class Encodable(ABC):
    @staticmethod
    @abstractmethod
    def decode(encoded: JSONObject | JSONArray) -> 'Encodable':
        pass

    @abstractmethod
    def encode(self) -> JSONObject | JSONArray:
        pass
