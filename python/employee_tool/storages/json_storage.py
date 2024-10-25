import json
import os
import logging
from typing import Any, List

from storages.storage_interface import StorageInterface


class JSONEmployeeStorage(StorageInterface):
    def __init__(self, filename: str = "employees.json") -> None:
        self.filename = filename

    def read(self) -> List[dict[str, Any]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                return data
        else:
            logging.error("File json not exist")
            return []

    def save(self, employee: dict[str, Any]) -> bool:
        try:
            if os.path.exists(self.filename):
                with open(self.filename, "r") as file:
                    existing_data = json.load(file)

                existing_data.append(employee)

                with open(self.filename, "w") as file:
                    json.dump(existing_data, file, indent=4)
            else:
                with open(self.filename, "w") as file:
                    json.dump([employee], file, indent=4)

            return True
        except Exception as e:
            logging.error(e)
            return False

    def delete(self) -> bool:
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
                return True
            else:
                return False
        except Exception as e:
            logging.error(e)
            return False

    def search(self, search_term: str) -> List[dict[str, Any]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

                results = [
                    emp for emp in data if search_term.lower() in emp["name"].lower()
                ]

                return results
        else:
            logging.error("Not found json file")
            return []
