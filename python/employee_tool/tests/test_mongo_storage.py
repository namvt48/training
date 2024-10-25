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

    def test_read_empty_collection(self) -> None:
        employees = self.storage.read()
        self.assertEqual([], employees)

    def test_search_no_results(self) -> None:
        self.storage.save(self.sample_data)
        results = self.storage.search("NonExistentName")
        self.assertEqual(0, len(results))

    def test_delete_empty_collection(self) -> None:
        success = self.storage.delete()
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()
