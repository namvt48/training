import json
import clickhouse_connect

client = clickhouse_connect.get_client(host='192.168.1.58', database='mempool_tracker')

print('Connecting to database...', client)
query_data = "select transaction_hash, to, node_id from transactions2 where received_at between 1734318612 and 1734402896"
result_query = client.query(query_data)

result = [data for data in result_query.result_rows]

with open("./data/pending_txs.json", 'w') as f:
    json.dump(result, f, indent=4)