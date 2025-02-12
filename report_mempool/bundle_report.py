import json
from collections import defaultdict

# BUNDLES_FILE = "./data/bundles.json"
BUNDLES_FILE = "./data/signals_uni.json"
PENDING_TXS_FILE = "./data/pending_txs.json"

def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Không tìm thấy file: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"File {file_path} không hợp lệ. Vui lòng kiểm tra lại định dạng JSON.")
        return None

def count_transactions_by_node(pending_txs):
    node_counts = defaultdict(int)
    for tx in pending_txs:
        if isinstance(tx, list) and len(tx) >= 3:
            transaction_hash, to, node_id = tx[:3]
            node_counts[node_id] += 1
        else:
            print(f"Dữ liệu giao dịch không hợp lệ: {tx}")
    return node_counts

def get_signal_txs(bundles):
    signal_txs = []
    for bundle in bundles:
        # signal = bundle.get("signalTxs")
        signal = bundle.get("_id")

        if signal:
            signal_txs.append(signal)
        else:
            print(f"Bundle không có trường 'signalTxs': {bundle}")
    return signal_txs

def count_matching_signals(signal_txs, pending_txs):
    signal_set = set(signal_txs)
    total_signals = len(signal_txs)

    matching_signals = 0

    signals_per_node = defaultdict(int)

    matched_signals_set = set()

    for tx in pending_txs:
        if isinstance(tx, list) and len(tx) >= 3:
            transaction_hash, to, node_id = tx[:3]
            if transaction_hash in signal_set:
                if transaction_hash not in matched_signals_set:
                    matching_signals += 1
                    matched_signals_set.add(transaction_hash)
                signals_per_node[node_id] += 1
        else:
            print(f"Dữ liệu giao dịch không hợp lệ: {tx}")

    return total_signals, matching_signals, signals_per_node

def main():
    bundles = load_json(BUNDLES_FILE)
    pending_txs = load_json(PENDING_TXS_FILE)

    if bundles is None or pending_txs is None:
        print("Không thể tải dữ liệu. Vui lòng kiểm tra lại các file JSON.")
        return

    node_counts = count_transactions_by_node(pending_txs)

    start = "2024-12-16 10:10:00"
    end = "2024-12-17 09:35:00"

    print(f"\n=== Thời gian từ {start} đến {end} ===")

    print("\n=== Số lượng transaction_hash ứng với từng node_id ===")
    print("------------------------------------------------------")
    for node_id, count in node_counts.items():
        print(f"Node ID: {node_id} => Số lượng giao dịch: {count}")

    signal_txs = get_signal_txs(bundles)
    total_signals, matching_signals, signals_per_node = count_matching_signals(signal_txs, pending_txs)

    print("\n=== Thống kê SignalTxs ===")
    print("---------------------------")
    print(f"Tổng số signalTxs trong bundles.json: {total_signals}")
    print(f"Số lượng signalTxs xuất hiện trong transaction_hash của pending_txs.json: {matching_signals}")
    percentage = (matching_signals / total_signals * 100) if total_signals > 0 else 0
    print(f"Tỷ lệ xuất hiện: {percentage:.2f}%")

    print("\n=== Phân bố số lượng SignalTxs xuất hiện theo node_id ===")
    print("-------------------------------------------------------------")
    for node_id, count in signals_per_node.items():
        print(f"Node ID: {node_id} => Số lượng SignalTxs xuất hiện: {count}, tỉ lệ: {count/total_signals * 100:.2f}%")

if __name__ == "__main__":
    main()
