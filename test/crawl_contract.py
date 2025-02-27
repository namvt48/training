import requests
import os
import json

def read_addresses_from_file(file_path):
    with open(file_path, 'r') as f:
        addresses = json.load(f)

    return addresses

def download_contract_sources(address_list, etherscan_api_key, output_folder="contracts"):
    base_url = "https://api.etherscan.io/api"

    for contract_address in address_list:
        params = {
            "module": "contract",
            "action": "getsourcecode",
            "address": contract_address,
            "apikey": etherscan_api_key
        }

        try:
            response = requests.get(base_url, params=params, timeout=10)
            data = response.json()

            if data["status"] == "1" and len(data["result"]) > 0:
                contract_info = data["result"][0]
                contract_name = contract_info["ContractName"].strip()
                source_code = contract_info["SourceCode"]

                if not contract_name:
                    contract_name = "UnknownContract"

                file_name = f"{contract_name}.sol"
                output_path = os.path.join(output_folder, file_name)

                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(source_code)

                print(f"save contract {contract_name} ({contract_address}) -> {output_path}")
            else:
                print(f"not found contract {contract_address}.")

        except Exception as e:
            print(f"error: {str(e)}")


if __name__ == "__main__":
    addresses_file = 'address.json'
    my_api_key = "K3KW9P4B6RT8C5T4PJMAQGBYK8KZ6UQF9D"

    addresses = read_addresses_from_file(addresses_file)
    download_contract_sources(addresses, my_api_key)
