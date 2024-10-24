import argparse
from typing import Optional, Any

from employee_manager import EmployeeManager
from storages import CSVEmployeeStorage, JSONEmployeeStorage, MongoEmployeeStorage


def main() -> None:
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
        choices=["json", "csv", "mongo"],
        default="json",
        help="Type of file",
    )

    parser.add_argument("--search_name", type=str, help="Name of employee for search")

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
            manager.search_employee(args.search_name)
        case "delete":
            manager.delete_file()


if __name__ == "__main__":
    main()
