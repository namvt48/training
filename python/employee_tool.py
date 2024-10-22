import argparse
import json
import csv
import os

parser = argparse.ArgumentParser("employee input tool")

parser.add_argument("--name", type=str, help="Name of employee", required=True)
parser.add_argument("--age", type=int, help="Age of employee", required=True)

parser.add_argument("--filetype", type=str, choices=["json", "csv"], default="json", help="Type of file")

args = parser.parse_args()

def save_to_json(data, filename="employees.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            exist_data = json.load(file)
        
        exist_data.append(data)

        with open(filename, "w") as file:
            json.dump(exist_data, file)
    else:
        with open(filename, "w") as file:
            json.dump([data], file)

    print("Data save to json file")

def save_to_csv(data, filename="employees.csv"):
    file_exist = os.path.exists(filename)

    with open(filename, "a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exist:
            writer.writeheader()
        writer.writerow(data)

    print("Data save to csv file")

input_data = {
    "name": args.name,
    "age": args.age
}

if args.filetype == "json":
    save_to_json(input_data)
else:
    save_to_csv(input_data)