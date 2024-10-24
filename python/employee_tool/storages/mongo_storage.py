from pymongo import MongoClient
from typing import Any, List
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

    def read(self) -> List[dict[str, Any]]:
        try:
            employees = list(self.collection.find())
            return employees
        except Exception as e:
            print(f"Error occur: {e}")
            return []

    def save(self, employee: dict[str, Any]) -> bool:
        try:
            self.collection.insert_one(employee)
            print(f"Store {employee} to MongoDB.")
            return True
        except Exception as e:
            print(f"Error occur: {e}")
            return False

    def delete(self) -> bool:
        try:
            self.collection.delete_many({})
            print("Delete data in MongoDB.")
            return True
        except Exception as e:
            print(f"Error occur: {e}")
            return False

    def search(self, search_term: str) -> List[dict[str, Any]]:
        try:
            query = {'name': {'$regex': search_term, '$options': 'i'}}
            results = list(self.collection.find(query))
            return results
        except Exception as e:
            print(f"Error occur: {e}")
            return []
