import argparse
import logging
from typing import Any

from employee_tool.manager.employee_manager import EmployeeManager
from employee_tool.storages import CSVEmployeeStorage, JSONEmployeeStorage, MongoEmployeeStorage


def main() -> None:
    parser = argparse.ArgumentParser(description="Employee input tool")

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    #Save parse
    save_parser = subparsers.add_parser("save", help="Save employee")
    save_parser.add_argument("--name", type=str, help="Name of employee")
    save_parser.add_argument("--age", type=int, help="Age of employee")
    save_parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv", "mongo"],
        default="json",
        help="Type of file to save",
    )

    #Read parse
    read_parser = subparsers.add_parser("read", help="Read employee")
    read_parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv", "mongo"],
        default="json",
        help="Type of file to read",
    )

    #Delete parse
    delete_parser = subparsers.add_parser("delete", help="Delete employee")
    delete_parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv", "mongo"],
        default="json",
        help="Type of file to delete",
    )

    #Search parse
    search_parser = subparsers.add_parser("search", help="Search employee")
    search_parser.add_argument("--search_name", type=str, help="Name of employee")
    search_parser.add_argument(
        "--filetype",
        type=str,
        choices=["json", "csv", "mongo"],
        default="json",
        help="Type of file to search",
    )

    args: Any = parser.parse_args()

    if args.filetype == "json":
        storage = JSONEmployeeStorage()
    elif args.filetype == "csv":
        storage = CSVEmployeeStorage()
    elif args.filetype == "mongo":
        storage = MongoEmployeeStorage()
    else:
        raise ValueError("Unsupported filetype")

    manager = EmployeeManager(storage)

    match args.command:
        case "read":
            employees = manager.read_employees()

            if not employees:
                logging.error("No employees found")
            else:
                print("List of employees:")
                for employee in employees:
                    print(employee)
        case "save":
            if args.name is not None and args.age is not None:
                try:
                    employee_data = {"name": args.name, "age": args.age}
                    is_success = manager.save_employee(employee_data)

                    if is_success:
                        print("Employee saved")
                    else:
                        logging.error("Employee not saved")
                except TypeError:
                    logging.error("Invalid arguments")
            else:
                logging.error("Missing arguments")

        case "search":
            employees = manager.search_employee(args.search_name)

            if not employees:
                logging.error("No employees found")
            else:
                print("List of employees:")
                for employee in employees:
                    print(employee)
        case "delete":
            is_success = manager.delete_file()

            if is_success:
                print("Employee deleted")
            else:
                logging.error("Employee not deleted")

if __name__ == "__main__":
    main()
