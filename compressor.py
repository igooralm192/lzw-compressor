import math, textwrap
from helper import byteToBin, fullByte

def encoding(filename: str, tam_bits: int, max_bits: int):
    bit_size = tam_bits+1
    max_size = (1 << tam_bits)
    dictionary = {}
    for i in range(max_size):
        dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i
    
    file = open(filename, "rb")
    result = open(filename.split('.')[0]+".cmp", "wb")

    file_bits = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        byte = byteToBin(byte, full=True)
        file_bits += byte

    file_bits = textwrap.wrap(file_bits, tam_bits)

    prefix = ""
    codes = []
    index = max_size

    for c in file_bits:
        p = prefix+c

        if p in dictionary:
            prefix = p
        else:
            codes.append(dictionary[prefix])
            dictionary[p] = index
            index += 1

            if index == max_size:
                bit_size += 1

            if bit_size > max_bits:
                bit_size = tam_bits+1
                max_size = (1 << tam_bits)
                dictionary = {}
                for i in range(max_size):
                    dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i
                index = max_size

            prefix = c
    
    codes.append(dictionary[fullByte(prefix, length=tam_bits)])

    bits = ''
    max_code = 0
    for code in codes:
        max_code = max(code, max_code)
    getbit_size = len(bin(max_code)[2:])

    for code in codes:
        code_byte = fullByte(bin(code)[2:], length=getbit_size)
        bits += code_byte
            
    byte_list = textwrap.wrap(bits, 8)

    result.write(getbit_size.to_bytes(1, byteorder='big'))

    for byte in byte_list:
        byteorder = 'big'
        if len(byte) < 8:
            byte = '1' + byte

        result.write(int(byte, 2).to_bytes(1, byteorder))
    
    result.close()
    file.close()
    return 1
