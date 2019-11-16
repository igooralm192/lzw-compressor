from helper import fullByte, toInt, binToByte, toByte
import textwrap

def decoding(filename: str, tam_bits: int, max_bits: int):
    bit_size = tam_bits+1
    max_size = (1 << tam_bits)
    dictionary = {}
    for i in range(max_size):
        dictionary[i] = [fullByte(bin(i)[2:], length=tam_bits)]

    file = open(filename, "rb")
    result = open(filename.split('.')[0], "wb")

    getbit_size = int.from_bytes(file.read(1), "big")
    byte_file = ''

    origin_byte = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        
        byte = bin(int.from_bytes(byte, "big"))[2:]
        origin_byte = byte
        byte = fullByte(byte)
        byte_file += byte

    byte_file = byte_file[:len(byte_file)-8] + origin_byte[1:]

    byte_file = textwrap.wrap(byte_file, getbit_size)

    prefix = []
    codes = []
    index = max_size

    i = 0
    index_file = 0

    if index_file < len(byte_file):
        c = byte_file[index_file]
        index_file += 1
        c = dictionary[toInt(c)]
        codes += c

    while True:
        if (i >= len(codes)):
            if index_file < len(byte_file):
                c = byte_file[index_file]
                index_file += 1
                c = toByte(int(c, 2))

                c_int = int.from_bytes(c, 'big')

                # c_bytes = int.from_bytes(c, "big")
                if c_int not in dictionary:
                    dictionary[index] = prefix + [prefix[0]]
                    c = dictionary[index]
                    
                    index += 1
                    codes += c
                    prefix = [codes[i]]
                    i += 1
                else:
                    c = dictionary[c_int]
                    codes += c
            else:
                break

        p = prefix
        p.append(codes[i])

        if p in dictionary.values():
            prefix = p
        else:
            dictionary[index] = p

            index += 1

            if index == max_size:
                bit_size += 1

            if bit_size > max_bits:
                bit_size = tam_bits+1
                dictionary = {}
                for i in range(max_size):
                    dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i
                index = max_size

            prefix = [codes[i]]
        
        i += 1

    codes = ''.join(codes)
    codes = textwrap.wrap(codes, 8)

    for code in codes:
        code = binToByte(code)
        result.write(code)
    
    result.close()
    file.close()
    return 1