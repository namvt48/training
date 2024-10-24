from pymongo import MongoClient
from typing import Any
from storages.storage_interface import StorageInterface


class MongoEmployeeStorage(StorageInterface):
    def __init__(
            self,
            db_name: str = 'employee_db',
            collection_name: str = 'employees',
            url: str = "mongodb+srv://namvt123:namvt123@cluster0.5sxuq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") -> None:
        self.client: MongoClient = MongoClient(url)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        # print(self.client.server_info())

    def read(self) -> None:
        employees = list(
            self.collection.find()
        )
        if not employees:
            print("Employees not found")
        else:
            for employee in employees:
                print(employee)

    def save(self, employee: dict[str, Any]) -> None:
        self.collection.insert_one(employee)
        print(f"Store {employee} to MongoDB.")

    def delete(self) -> None:
        self.collection.delete_many({})
        print("Delete data in MongoDB.")

    def search(self, search_term: str) -> None:
        query = {
            'name': {'$regex': search_term, '$options': 'i'}
        }
        results = list(
            self.collection.find(query)
        )

        for employee in results:
            print(employee)