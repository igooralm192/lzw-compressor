import math, textwrap
from helper import byteToBin, fullByte, binToByte

def encoding(file_bits: str, tam_bits: int, max_bits: int, len_temp_file: int):
    print('Gerando dicionario...')
    bit_size = tam_bits+1
    max_size = (1 << tam_bits)
    dictionary = {}
    for i in range(max_size):
        dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i

    prefix = ""
    codes = []
    index = max_size

    print('Comprimindo...')
    max_original_code = 0

    for i in range(math.ceil(len(file_bits) / tam_bits)):
        c = file_bits[i*tam_bits:i*tam_bits+tam_bits]

        max_original_code = max(int(c, 2), max_original_code)
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

    print('Configurando saida...')
    bits = ''
    max_code = 0
    
    for code in codes:
        max_code = max(code, max_code)
    getbit_size = len(bin(max_code)[2:])

    for code in codes:
        code_byte = fullByte(bin(code)[2:], length=getbit_size)
        bits += code_byte
    
    if len(bits) > len(file_bits):
        print('Taxa de compressao: 0%')
        bits = file_bits
        # codes = textwrap.wrap(bits, tam_bits)
        getbit_size = len(bin(max_original_code)[2:])
    else:
        taxa = 1-(len(bits)/len(file_bits))
        taxa *= 100
        print('Taxa de compressao: ', taxa, '%')

    if len_temp_file > len(bits) or len_temp_file == 0:
        return True, [bits, fullByte(bin(tam_bits)[2:])[3:], fullByte(bin(max_bits)[2:])[3:], fullByte(bin(getbit_size)[2:])[3:]]
    else:
        return False, [None, None, None, None]
