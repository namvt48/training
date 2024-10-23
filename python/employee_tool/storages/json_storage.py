import json
import os


class JSONEmployeeStorage:
    def __init__(self, filename="employees.json"):
        self.filename = filename

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                print("List of employees from json file:")
                for emp in data:
                    print(emp)
        else:
            print("File json not exist")

    def save(self, employee):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                existing_data = json.load(file)

            existing_data.append(employee)

            with open(self.filename, "w") as file:
                json.dump(existing_data, file, indent=4)
        else:
            with open(self.filename, "w") as file:
                json.dump([employee], file, indent=4)
        print("Data save to json file")

    def delete(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Deleted file {self.filename}")
        else:
            print("File not found")

    def search(self, search_term):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)

                results = [
                    emp for emp in data if search_term.lower() in emp["name"].lower()
                ]

                if results:
                    print("Search result from json file:")
                    print(results)
                else:
                    print("Not found fom json file")
        else:
            print("Not found json file")
