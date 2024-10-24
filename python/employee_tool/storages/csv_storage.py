import csv
import os
from typing import Any, List

from storages.storage_interface import StorageInterface


class CSVEmployeeStorage(StorageInterface):
    def __init__(self, filename: str = "employees.csv") -> None:
        self.filename = filename

    def read(self) -> List[dict[str, Any]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                return list(reader)
        else:
            print("File csv not exist")
            return []

    def save(self, employee: dict[str, Any]) -> bool:
        try:
            fieldnames = ["name", "age"]
            file_exists = os.path.exists(self.filename)
            with open(self.filename, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()
                writer.writerow(employee)

            return True
        except Exception as e:
            print(f"Error occur: {e}")
            return False

    def delete(self) -> bool:
        try:
            if os.path.exists(self.filename):
                os.remove(self.filename)
                return True
            else:
                return False
        except Exception as e:
            print(f"Error occur: {e}")
            return False

    def search(self, search_term: str) -> List[dict[str, Any]]:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)

                results = [
                    row for row in reader if search_term.lower() in row["name"].lower()
                ]

                return results
        else:
            print("Not found csv file")
            return []
