import csv
import os
from typing import Any

from storages.storage_interface import StorageInterface


class CSVEmployeeStorage(StorageInterface):
    def __init__(self, filename: str = "employees.csv") -> None:
        self.filename = filename

    def read(self) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                print("List of employees from csv file:")
                for row in reader:
                    print(row)
        else:
            print("File csv not exist")

    def save(self, employee: dict[str, Any]) -> None:
        fieldnames = ["name", "age"]
        file_exists = os.path.exists(self.filename)
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow(employee)
        print("Data save to csv file")

    def delete(self) -> None:
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Deleted file {self.filename}")
        else:
            print("File not found")

    def search(self, search_term: str) -> None:
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                reader = csv.DictReader(file)

                results = [
                    row for row in reader if search_term.lower() in row["name"].lower()
                ]

                if results:
                    print("Search result from csv file:")
                    print(results)
                else:
                    print("Not found from csv file")
        else:
            print("Not found csv file")
