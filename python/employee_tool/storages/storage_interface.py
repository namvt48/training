from abc import ABC, abstractmethod
from typing import Any


class StorageInterface(ABC):
    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def save(self, employ: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def delete(self) -> None:
        pass

    @abstractmethod
    def search(self, search_term: str) -> None:
        pass
