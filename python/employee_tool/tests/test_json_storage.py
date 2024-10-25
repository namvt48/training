import unittest
import os
from storages.json_storage import JSONEmployeeStorage


class TestJSONEmployeeStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.storage = JSONEmployeeStorage('test_employees.json')
        self.sample_data = {"name": "Nguyen Van A", "age": 30}

    def tearDown(self) -> None:
        if os.path.exists('test_employees.json'):
            os.remove('test_employees.json')

    def test_save_and_read(self) -> None:
        self.storage.save(self.sample_data)
        employees = self.storage.read()
        self.assertEqual(1, len(employees))
        self.assertEqual("Nguyen Van A", employees[0]['name'])

    def test_delete(self) -> None:
        self.storage.save(self.sample_data)
        self.storage.delete()
        employees = self.storage.read()
        self.assertEqual(0, len(employees))

    def test_search(self) -> None:
        self.storage.save(self.sample_data)
        results = self.storage.search("Nguyen")
        self.assertEqual(1, len(results))
        self.assertEqual("Nguyen Van A", results[0]['name'])

    def test_read_non_existing_file(self) -> None:
        self.storage = JSONEmployeeStorage('test_non_existing_file.json')
        result = self.storage.read()
        self.assertEqual([], result)

    def test_delete_non_existing_file(self) -> None:
        storage = JSONEmployeeStorage('non_existing.json')
        success = storage.delete()
        self.assertFalse(success)

    def test_search_non_existing_file(self) -> None:
        storage = JSONEmployeeStorage('non_existing.json')
        results = storage.search("Nguyen")
        self.assertEqual([], results)

if __name__ == '__main__':
    unittest.main()
