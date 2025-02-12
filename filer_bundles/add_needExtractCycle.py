import json
from pymongo import MongoClient

# Hàm kết nối đến MongoDB
def connect_to_mongo(uri, db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    return collection

# Hàm đọc danh sách _id từ file JSON
def read_ids_from_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return [entry["_id"] for entry in data]

# Hàm cập nhật các document trong MongoDB
def update_transactions(collection, transaction_ids):
    for transaction_id in transaction_ids:
        result = collection.update_one(
            {"_id": transaction_id},  # Điều kiện tìm kiếm
            {"$set": {"needExtractCycles": True}}  # Trường cần cập nhật
        )
        print(f"Updated _id {transaction_id}: Matched {result.matched_count}, Modified {result.modified_count}")

# Hàm main
def main():
    # Thông tin kết nối MongoDB
    MONGO_URI = "mongodb://192.168.1.58:27018/"  # Thay bằng URI thực tế của bạn
    DATABASE_NAME = "mev"
    COLLECTION_NAME = "transactions"

    # Đường dẫn tới file JSON
    JSON_FILE_PATH = "data/total_searchers.json"  # Thay bằng đường dẫn file JSON thực tế của bạn

    # Kết nối đến MongoDB
    collection = connect_to_mongo(MONGO_URI, DATABASE_NAME, COLLECTION_NAME)

    # Đọc danh sách _id từ file JSON
    transaction_ids = read_ids_from_json(JSON_FILE_PATH)

    # Cập nhật các transaction trong MongoDB

    # print(transaction_ids)
    update_transactions(collection, transaction_ids)

if __name__ == "__main__":
    main()
