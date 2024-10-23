class EmployeeManager:
    def __init__(self, storage):
        self.storage = storage

    def read_employees(self):
        self.storage.read()

    def save_employee(self, employee):
        self.storage.save(employee)

    def delete_file(self):
        self.storage.delete()

    def search_employee(self, search_term):
        self.storage.search(search_term)
