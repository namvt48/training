import json
import clickhouse_connect

client = clickhouse_connect.get_client(host='192.168.1.58', database='mempool_tracker')

print('Connecting to database...', client)
query_data_max = "select max(received_at) from transactions2"
query_data_min = "select min(received_at) from transactions2"

result_max = client.query(query_data_max)
result_min = client.query(query_data_min)

time_max = result_max.result_rows
time_min = result_min.result_rows

print("time max: ", time_max)
print("time min: ", time_min)