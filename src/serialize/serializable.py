from abc import ABC, abstractmethod


class Serializable(ABC):
    @staticmethod
    @abstractmethod
    def from_json(s: str) -> 'Serializable':
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass
