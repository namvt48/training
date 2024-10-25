import os
import logging
from pymongo import MongoClient
from typing import Any, List
from employee_tool.storages.storage_interface import StorageInterface
from dotenv import load_dotenv


class MongoEmployeeStorage(StorageInterface):
    def __init__(
            self,
            db_name: str = 'employee_db',
            collection_name: str = 'employees',
    ) -> None:
        try:
            load_dotenv()
            self.client: MongoClient = MongoClient(os.getenv('MONGO_URI'))
            self.db = self.client[db_name]
            self.collection = self.db[collection_name]
        except Exception as e:
            logging.error(f"Error connecting to Mongo DB {e}")

    def read(self) -> List[dict[str, Any]]:
        try:
            employees = list(self.collection.find())
            return employees
        except Exception as e:
            logging.error(f"Error reading from Mongo DB {e}")
            return []

    def save(self, employee: dict[str, Any]) -> bool:
        try:
            self.collection.insert_one(employee)
            print(f"Store {employee} to MongoDB.")
            return True
        except Exception as e:
            logging.error(f"Error writing to Mongo DB {e}")
            return False

    def delete(self) -> bool:
        try:
            self.collection.delete_many({})
            print("Delete data in MongoDB.")
            return True
        except Exception as e:
            logging.error(f"Error deleting from Mongo DB {e}")
            return False

    def search(self, search_term: str) -> List[dict[str, Any]]:
        try:
            query = {'name': {'$regex': search_term, '$options': 'i'}}
            results = list(self.collection.find(query))
            return results
        except Exception as e:
            logging.error(f"Error searching from Mongo DB {e}")
            return []

    # close mongo connection
    def close(self) -> None:
        self.client.close()
