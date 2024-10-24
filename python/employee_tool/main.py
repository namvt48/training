import argparse
from typing import Optional, Any

from employee_manager import EmployeeManager
from storages import CSVEmployeeStorage, JSONEmployeeStorage, MongoEmployeeStorage


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
