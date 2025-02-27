from web3 import Web3

provider_url = "http://192.168.1.58:8545"
w3 = Web3(Web3.HTTPProvider(provider_url))


def bytes_to_uint256(data_bytes):
    return int.from_bytes(data_bytes, byteorder='big')


def get_storage_at_slot(contract_address, slot_index):
    return w3.eth.get_storage_at(contract_address, slot_index)


def get_mapping_value(contract_address, mapping_key, slot_index):
    key_hash = Web3.keccak(text=str(mapping_key))
    storage_slot = Web3.keccak(key_hash + Web3.to_bytes(hexstr=str(slot_index)))

    return w3.eth.get_storage_at(contract_address, storage_slot).hex()


def main():
    contract_address = "0xa2b4c0af19cc16a6cfacce81f192b024d625817d"
    contract_address = w3.to_checksum_address(contract_address)

    slot_index = 7
    mapping_key = "0x1FfA62DBeC4E6765A18A3056279e9Bc5d812D118"
    print(f"Truy xuất giá trị tại slot {slot_index}...")
    slot_map_value = get_storage_at_slot(contract_address, slot_index)

    print(f"Giá trị tại slot {slot_index}: {bytes_to_uint256(slot_map_value)}")


if __name__ == "__main__":
    main()
