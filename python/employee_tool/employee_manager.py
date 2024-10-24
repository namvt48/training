from typing import Any

from storages.storage_interface import StorageInterface


class EmployeeManager:
    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage

    def read_employees(self) -> None:
        self.storage.read()

    def save_employee(self, employee: dict[str, Any]) -> None:
        self.storage.save(employee)

    def delete_file(self) -> None:
        self.storage.delete()

    def search_employee(self, search_term: str) -> None:
        self.storage.search(search_term)
