import json
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor


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
        return data


# Hàm xử lý một bundle
def process_bundle(bundle_collection, transaction_collection, bundle_id, valid_bundle_ids):
    bundle = bundle_collection.find_one({"_id": bundle_id})
    if bundle:
        signal_txs = bundle.get("signalTxs", [])

        # Kiểm tra signalTxs có đúng 1 phần tử
        if len(signal_txs) == 1:
            signal_tx_id = signal_txs[0]
            print("process tx: ", signal_tx_id)
            # Tìm transaction trong collection transaction
            transaction = transaction_collection.find_one({"_id": signal_tx_id})
            if transaction:
                contract_name = transaction.get("contractName", "")

                # Kiểm tra contractName có thuộc danh sách cho phép
                if contract_name in ["UniversalRouter", "UniswapV2Router02", "UniswapV3Router", "UniswapV3Router2"]:
                    valid_bundle_ids.append(bundle_id)


# Hàm lọc các bundle và transaction sử dụng đa luồng
def filter_bundles_and_transactions_multithreaded(bundle_collection, transaction_collection, transaction_ids,
                                                  max_workers=10):
    valid_bundle_ids = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(process_bundle, bundle_collection, transaction_collection, bundle_id, valid_bundle_ids)
            for bundle_id in transaction_ids
        ]
        for future in futures:
            future.result()

    return valid_bundle_ids


# Hàm lưu dữ liệu vào file JSON
def save_to_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)


# Hàm main
def main():
    # Thông tin kết nối MongoDB
    MONGO_URI = "mongodb://192.168.1.58:27018/"  # Thay bằng URI thực tế của bạn
    DATABASE_NAME = "mev"
    BUNDLE_COLLECTION_NAME = "bundles_1_2025"
    TRANSACTION_COLLECTION_NAME = "transactions"

    # Đường dẫn tới file JSON
    INPUT_JSON_FILE = "./output/filtered_searcher.json"  # Thay bằng đường dẫn file JSON thực tế của bạn
    OUTPUT_JSON_FILE = "output/filtered_signal.json"  # Tên file đầu ra

    # Kết nối đến MongoDB
    bundle_collection = connect_to_mongo(MONGO_URI, DATABASE_NAME, BUNDLE_COLLECTION_NAME)
    transaction_collection = connect_to_mongo(MONGO_URI, DATABASE_NAME, TRANSACTION_COLLECTION_NAME)

    # Đọc danh sách _id từ file JSON
    transaction_ids = read_ids_from_json(INPUT_JSON_FILE)

    # Lọc các bundle và transactions thỏa mãn điều kiện sử dụng đa luồng
    valid_bundle_ids = filter_bundles_and_transactions_multithreaded(bundle_collection, transaction_collection,
                                                                     transaction_ids)

    # Lưu bundleIds vào file JSON
    save_to_json(valid_bundle_ids, OUTPUT_JSON_FILE)
    print(f"Filtered bundleIds have been saved to {OUTPUT_JSON_FILE}")


if __name__ == "__main__":
    main()
