import json
from collections import Counter
import pymongo

db = pymongo.MongoClient(host="localhost", port=27017)['mev']

with open("data/bundles.json") as f:
    signals = json.load(f)

signal_tx = [sig['signalTxs'] for sig in signals]

collection = db['transactions']

pipeline = [
    {
        "$unwind": "$types"
    },
    {
        "$match": {
            "types": "arbitrage"
        }
    },
    {
        "$addFields": {
            "to": "$raw.to"
        }
    },
    {
        "$project": {
            "_id": 1,
            "to": 1
        }
    },
    {
        "$match": {
            "_id": {"$in": signal_tx},
        }
    },
]

id_tx = collection.aggregate(pipeline)
addresses = [item for item in id_tx]  # Đảm bảo tất cả địa chỉ đều ở dạng chữ thường

print(addresses)

allowed_addresses = {
    "0xf164fc0ec4e93095b804a4795bbe1e041497b92a",  # uniswapv2router01
    "0x7a250d5630b4cf539739df2c5dacb4c659f2488d",  # uniswapv2router02
    "0xef1c6e67703c7bd7107eed8303fbe6ec2554bf6b",  # universalrouter
    "0x3fc91a3afd70395cd496c647d5a6cc9d4b2b7fad",  # universalrouterv1_2
    "0xe592427a0aece92de3edee1f18e0157c05861564",  # swaprouter
    "0x68b3465833fb72a70ecdf485e0e4c7bd8665fc45",  # swaprouter02
}

result = [add for add in addresses if add['to'] in allowed_addresses]

with open("data/signals_uni.json", "w") as f:
    json.dump(result, f, indent=2)

# print(result)

# # Đếm số lần xuất hiện của từng địa chỉ
# address_counts = Counter(addresses)
#
# # Định nghĩa tập hợp các địa chỉ cần lọc (sử dụng chữ thường để đảm bảo so sánh chính xác)
#
#
# # Lọc các địa chỉ chỉ giữ lại những địa chỉ trong allowed_addresses
# filtered_counts = {addr: count for addr, count in address_counts.items() if addr in allowed_addresses}
#
# # Tính tổng số địa chỉ ban đầu để tính tỷ lệ phần trăm
# total_addresses = len(addresses)
#
# # In kết quả với tỷ lệ phần trăm
# for addr, count in filtered_counts.items():
#     percentage = (count / total_addresses) * 100
#     print(f"{addr}: {percentage:.2f}%")

