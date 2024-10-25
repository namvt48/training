from abc import ABC, abstractmethod
from typing import Any, List


class StorageInterface(ABC):
    @abstractmethod
    def read(self) -> List[dict[str, Any]]:
        pass

    @abstractmethod
    def save(self, employ: dict[str, Any]) -> bool:
        pass

    @abstractmethod
    def delete(self) -> bool:
        pass

    @abstractmethod
    def search(self, search_term: str) -> List[dict[str, Any]]:
        pass
