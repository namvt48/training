from web3 import Web3

# Thay bằng URL của node bạn (Infura, Alchemy, hay node local)
provider_url = "https://mainnet.infura.io/v3/<YOUR_INFURA_KEY>"
w3 = Web3(Web3.HTTPProvider(provider_url))

# Địa chỉ contract (đã triển khai trên blockchain)
contract_address = "0x1234567890ABCDEF1234567890aBcDeF12345678"
contract_address = w3.toChecksumAddress(contract_address)


def read_storage_slot(addr, slot_index):
    # getStorageAt trả về dữ liệu bytes (hex)
    data_bytes = w3.eth.getStorageAt(addr, slot_index)
    return data_bytes


def bytes_to_uint256(data_bytes):
    # Chuyển từ 32 bytes big-endian -> số nguyên
    return int.from_bytes(data_bytes, byteorder='big')


def bytes_to_address(data_bytes):
    # Address là 20 bytes cuối, parse từ 32 bytes
    # Thường ta lấy 12 byte đầu bỏ đi, 20 byte còn lại là address
    addr_int = int.from_bytes(data_bytes[12:], byteorder='big')
    return Web3.toChecksumAddress(addr_int.to_bytes(20, 'big'))


def decode_bool_slot22(slot_bytes):
    """
    3 biến bool: tradingOpen, inSwap, swapEnabled
    Mỗi biến chiếm 1 byte, theo thứ tự khai báo.
    Byte thấp nhất (offset 0) dành cho tradingOpen,
    tiếp theo (offset 1) cho inSwap,
    tiếp theo (offset 2) cho swapEnabled.
    """
    # Chuyển thành int 256-bit
    slot_val = int.from_bytes(slot_bytes, byteorder='big')

    # Lấy từng byte
    tradingOpen_byte = (slot_val >> (0 * 8)) & 0xFF
    inSwap_byte = (slot_val >> (1 * 8)) & 0xFF
    swapEnabled_byte = (slot_val >> (2 * 8)) & 0xFF

    # Diễn giải 0 => False, !=0 => True
    tradingOpen = (tradingOpen_byte != 0)
    inSwap = (inSwap_byte != 0)
    swapEnabled = (swapEnabled_byte != 0)

    return tradingOpen, inSwap, swapEnabled


# Danh sách (slot, tên biến, kiểu dữ liệu) để in cho gọn
variables = [
    (3, "_taxWallet", "address"),
    (4, "_teamWallet", "address"),
    (5, "_taxWalletPercentage", "uint256"),
    (6, "_teamWalletPercentage", "uint256"),
    (7, "firstBlock", "uint256"),

    (8, "_initialBuyTax", "uint256"),
    (9, "_initialSellTax", "uint256"),
    (10, "_finalBuyTax", "uint256"),
    (11, "_finalSellTax", "uint256"),
    (12, "_reduceBuyTaxAt", "uint256"),
    (13, "_reduceSellTaxAt", "uint256"),
    (14, "_preventSwapBefore", "uint256"),
    (15, "_buyCount", "uint256"),

    (16, "_maxTxAmount", "uint256"),
    (17, "_maxWalletSize", "uint256"),
    (18, "_taxSwapThreshold", "uint256"),
    (19, "_maxTaxSwap", "uint256"),

    (20, "uniswapV2Router", "address"),
    (21, "uniswapV2Pair", "address"),
    # Slot 22 chứa 3 bool: tradingOpen, inSwap, swapEnabled
]

print("Reading storage from contract:", contract_address)
for (slot_idx, var_name, var_type) in variables:
    raw_bytes = read_storage_slot(contract_address, slot_idx)

    if var_type == "uint256":
        val = bytes_to_uint256(raw_bytes)
        print(f"{var_name} (slot {slot_idx}): {val}")
    elif var_type == "address":
        val = bytes_to_address(raw_bytes)
        print(f"{var_name} (slot {slot_idx}): {val}")
    else:
        print(f"{var_name} (slot {slot_idx}): Unhandled type")

# Đọc riêng slot 22 (chứa 3 bool)
slot22_bytes = read_storage_slot(contract_address, 22)
(tradingOpen, inSwap, swapEnabled) = decode_bool_slot22(slot22_bytes)

print(f"tradingOpen (slot 22): {tradingOpen}")
print(f"inSwap      (slot 22): {inSwap}")
print(f"swapEnabled (slot 22): {swapEnabled}")
