from eth_abi.abi import encode
from web3 import Web3
import json

# Dữ liệu đầu vào của bạn
input_data = {
    "method": None,
    "types": [
        "address",
        "address"
    ],
    "inputs": [
        "0x0000000000000000000000000000000000000060",
        "0xb10cc888cB2CcE7036F4c7ECAd8a57Da16161338"
    ],
    "names": [
        "_factory",
        "_WETH9"
    ]
}

# Đọc ABI từ file
with open('abi.json', 'r') as abi_file:
    abi = json.load(abi_file)

# Tạo đối tượng Web3
w3 = Web3()

# Hàm để mã hóa dữ liệu constructor
def encode_constructor_input(input_data):
    types = input_data.get("types", [])
    inputs = input_data.get("inputs", [])

    if len(types) != len(inputs):
        raise ValueError("Số lượng types và inputs phải bằng nhau.")

    # Sử dụng eth_abi để mã hóa các tham số
    try:
        encoded = encode(types, inputs)
        data_hex = '0x' + encoded.hex()
        return data_hex
    except Exception as e:
        raise ValueError(f"Lỗi khi mã hóa dữ liệu: {e}")

# Sử dụng hàm để mã hóa dữ liệu
try:
    if input_data.get("method") is None:
        # Mã hóa constructor
        input_hex = encode_constructor_input(input_data)
        print("Constructor Input Data (Hex):", input_hex)
    else:
        # Nếu method không phải là None, mã hóa cho một hàm cụ thể
        # Sẽ cần thêm thông tin về hàm để thực hiện mã hóa
        method = input_data["method"]
        types = input_data["types"]
        inputs = input_data["inputs"]

        # Tạo đối tượng Contract
        contract = w3.eth.contract(abi=abi)

        # Mã hóa dữ liệu cho hàm cụ thể
        try:
            function = getattr(contract.functions, method)
            encoded_data = function(*inputs).build_transaction()['data']
            print("Function Input Data (Hex):", encoded_data)
        except AttributeError:
            raise ValueError(f"Hàm '{method}' không tồn tại trong ABI.")
except Exception as e:
    print("Lỗi:", e)
