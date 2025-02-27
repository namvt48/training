def decode_rs(num: int):
    bit_length = num.bit_length() + 1
    uint32_bits = 32
    u112_bits = 112

    ts = num >> (bit_length - uint32_bits)
    shift_for_second_part = bit_length - uint32_bits - u112_bits
    rs1 = (num >> shift_for_second_part) & ((1 << u112_bits) - 1)
    rs0 = num & ((1 << u112_bits) - 1)

    return ts, rs0, rs1


if __name__ == '__main__':
    ts, rs0, rs1 = decode_rs(46581680090220587206421041498268903064418489187620886694340276250372582562146)
    print(f"ts: {ts}, rs0: {rs0}, rs1: {rs1}")