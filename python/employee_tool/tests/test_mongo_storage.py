import unittest
from storages.mongo_storage import MongoEmployeeStorage

class TestMongoEmployeeStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = MongoEmployeeStorage(db_name='test_employee_db', collection_name='test_employees')
        self.sample_data = {"name": "Nguyen Van A", "age": 30}

        self.storage.delete()

    def tearDown(self) -> None:
        self.storage.delete()
        self.storage.close()
        # self.storage.client.drop_database('test_employee_db')

    def test_save_and_read(self) -> None:
        self.storage.save(self.sample_data)
        employees = self.storage.read()
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0]['name'], "Nguyen Van A")

    def test_delete(self) -> None:
        self.storage.save(self.sample_data)
        self.storage.delete()
        employees = self.storage.read()
        self.assertEqual(len(employees), 0)

    def test_search(self) -> None:
        self.storage.save(self.sample_data)
        results = self.storage.search("Nguyen")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], "Nguyen Van A")


if __name__ == '__main__':
    unittest.main()
