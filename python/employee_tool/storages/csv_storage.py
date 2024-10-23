import csv
import os


class CSVEmployeeStorage:
    def __init__(self, filename="employees.csv"):
        self.filename = filename

    def read(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", newline="") as file:
                reader = csv.DictReader(file)
                print("List of employees from csv file:")
                for row in reader:
                    print(row)
        else:
            print("File csv not exist")

    def save(self, employee):
        fieldnames = ["name", "age"]
        file_exists = os.path.exists(self.filename)
        with open(self.filename, "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()

            writer.writerow(employee)
        print("Data save to csv file")

    def delete(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            print(f"Deleted file {self.filename}")
        else:
            print("File not found")

    def search(self, search_term):
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
