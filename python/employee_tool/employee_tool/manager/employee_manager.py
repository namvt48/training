from typing import Any, List

from employee_tool.storages.storage_interface import StorageInterface


class EmployeeManager:
    def __init__(self, storage: StorageInterface) -> None:
        self.storage = storage

    def read_employees(self) -> List[dict[str, Any]]:
        return self.storage.read()

    def save_employee(self, employee: dict[str, Any]) -> bool:
        return self.storage.save(employee)

    def delete_file(self) -> bool:
        return self.storage.delete()

    def search_employee(self, search_term: str) -> List[dict[str, Any]]:
        return self.storage.search(search_term)
