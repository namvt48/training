import pymongo
import json
import csv
from collections import Counter

client = pymongo.MongoClient("mongodb://192.168.1.58:27018/")
db = client["mev"]
bundle_collection = db["bundles_10_2024"]
transactions_collection = db["transactions"]

with open("data.json", "r") as file:
    data = json.load(file)

hashes = data["hashes"]

token_counter = Counter()

for hash_value in hashes:
    bundle_doc = bundle_collection.find_one({"_id": hash_value})
    if bundle_doc and "signalTxs" in bundle_doc:
        signal_tx = bundle_doc["signalTxs"][0]

        transaction_doc = transactions_collection.find_one({"_id": signal_tx})
        if transaction_doc and "tokens" in transaction_doc:
            tokens = transaction_doc["tokens"]

            token_counter.update(tokens)

sorted_tokens = sorted(token_counter.items(), key=lambda x: x[1], reverse=True)

with open("tokens_count.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Token", "Count"])  # Header

    for token, count in sorted_tokens:
        writer.writerow([token, count])

print("Data saved to tokens_count.csv")