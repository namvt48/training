import unittest
import os
from storages.csv_storage import CSVEmployeeStorage

class TestCsvEmployeeStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = CSVEmployeeStorage('test_employees.csv')
        self.sample_data = {"name": "Nguyen Van A", "age": 30}

    def tearDown(self) -> None:
        if os.path.exists('test_employees.csv'):
            os.remove('test_employees.csv')

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
    print("Test csv storage:")
    unittest.main()
