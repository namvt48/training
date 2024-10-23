import argparse
import csv
import json
import os

# read data from file
# python3 employee_tool_v2.py read --filetype csv

# save new employee
# python3 employee_tool_v2.py save --filetype json --name "Nguyen Van A" --age 30

# search employee by name
# python3 employee_tool_v2.py search --filetype csv --search_name abc

# delete file
# python3 employee_tool_v2.py delete --filetype json


class EmployeeManager:
    def __init__(self, filetype="json"):
        self.filetype = filetype
        self.json_filename = "employees.json"
        self.csv_filename = "employees.csv"

    def get_filename(self):
        if self.filetype == "json":
            return self.json_filename
        elif self.filetype == "csv":
            return self.csv_filename

    def read_employees(self):
        filename = self.get_filename()

        if self.filetype == "json":
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    data = json.load(file)
                    print(data)
                    print("List of employees from json file:")
                    for emp in data:
                        print(emp)
            else:
                print("File json not exist")

        elif self.filetype == "csv":
            if os.path.exists(filename):
                with open(filename, "r", newline="") as file:
                    reader = csv.DictReader(file)
                    print("List of employees from csv file:")
                    for row in reader:
                        print(row)
            else:
                print("File csv not exist")

    def save_employee(self, employee):
        fieldnames = ["name", "age"]
        filename = self.get_filename()

        if self.filetype == "json":
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    existing_data = json.load(file)

                existing_data.append(employee)

                with open(filename, "w") as file:
                    json.dump(existing_data, file, indent=4)
            else:
                with open(filename, "w") as file:
                    json.dump([employee], file, indent=4)
            print("Data save to json file")
        elif self.filetype == "csv":
            file_exists = os.path.exists(filename)
            with open(filename, "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if not file_exists:
                    writer.writeheader()

                writer.writerow(employee)
            print("Data save to csv file")

    def search_employees(self, search_term):
        filename = self.get_filename()

        if self.filetype == "json":
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    data = json.load(file)

                    results = [
                        emp
                        for emp in data
                        if search_term.lower() in emp["name"].lower()
                    ]

                    if results:
                        print("Search result from json file:")
                        print(results)
                    else:
                        print("Not found fom json file")
            else:
                print("Not found json file")
        elif self.filetype == "csv":
            if os.path.exists(filename):
                with open(filename, "r") as file:
                    reader = csv.DictReader(file)

                    results = [
                        row
                        for row in reader
                        if search_term.lower() in row["name"].lower()
                    ]

                    if results:
                        print("Search result from csv file:")
                        print(results)
                    else:
                        print("Not found from csv file")
            else:
                print("Not found csv file")

    def delete_file(self):
        filename = self.get_filename()

        if os.path.exists(filename):
            os.remove(filename)
            print(f"Deleted file {filename}")
        else:
            print("File not found")


def main():
    parser = argparse.ArgumentParser(description="employee input tool")

    parser.add_argument(
        "command",
        choices=["read", "save", "delete", "search"],
        help="Command for read, save, delete, search option",
    )

    parser.add_argument("--name", type=str, help="Name of employee")
    parser.add_argument("--age", type=int, help="Age of employee")

    parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv"],
        default="json",
        help="Type of file",
    )

    parser.add_argument("--search_name", type=str, help="Name of employee for search")

    args = parser.parse_args()

    manager = EmployeeManager(filetype=args.filetype)

    match args.command:
        case "read":
            manager.read_employees()
        case "save":
            if args.name is not None and args.age is not None:
                try:
                    employee_data = {"name": args.name, "age": args.age}

                    manager.save_employee(employee_data)
                except TypeError:
                    print("Invalid argument.")
            else:
                print("Employee's name or age is missing.")

        case "search":
            manager.search_employees(args.search_name)
        case "delete":
            manager.delete_file()


if __name__ == "__main__":
    main()