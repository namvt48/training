import json
from pymongo import MongoClient

# Hàm kết nối đến MongoDB
def connect_to_mongo(uri, db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

def read_ids_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [entry["_id"] for entry in data]

def filter_transactions(collection, transaction_ids):
    filtered_bundle_ids = []

    for transaction_id in transaction_ids:
        transaction = collection.find_one({"_id": transaction_id})
        print("filter tx: ", transaction_id)
        if transaction:
            bundle_ids = transaction.get("bundleIds", [])
            cycles = transaction.get("cycles", [])

            if len(bundle_ids) == 1 and len(cycles) == 1:
                filtered_bundle_ids.append(bundle_ids[0])

    return filtered_bundle_ids

# Hàm lưu dữ liệu vào file JSON
def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

# Hàm main
def main():
    MONGO_URI = "mongodb://192.168.1.58:27018/"
    DATABASE_NAME = "mev"
    COLLECTION_NAME = "transactions"

    INPUT_JSON_FILE = "data/total_searchers.json"
    OUTPUT_JSON_FILE = "./output/filtered_searcher.json"

    collection = connect_to_mongo(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    transaction_ids = read_ids_from_json(INPUT_JSON_FILE)

    filtered_bundle_ids = filter_transactions(collection, transaction_ids)

    save_to_json(filtered_bundle_ids, OUTPUT_JSON_FILE)
    print(f"Filtered bundleIds have been saved to {OUTPUT_JSON_FILE}")

if __name__ == "__main__":
    main()
