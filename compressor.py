import math, textwrap
from helper import byteToBin, fullByte
# from mata54comp import TEMP_FILE_BITS

def encoding(filename: str, tam_bits: int, max_bits: int):
    print('Gerando dicionario...')
    bit_size = tam_bits+1
    max_size = (1 << tam_bits)
    dictionary = {}
    for i in range(max_size):
        dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i
    
    file = open(filename, "rb")
    result = open(filename.split('.')[0]+".cmp", "wb")

    print('Analisando arquivo...')
    file_bits = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        byte = byteToBin(byte, full=True)
        file_bits += byte

    # list_bits = textwrap.wrap(file_bits, tam_bits)

    prefix = ""
    codes = []
    index = max_size

    print('Comprimindo...')
    max_original_code = 0

    for i in range(math.ceil(len(file_bits) / tam_bits)):
        c = file_bits[i*tam_bits:i*tam_bits+tam_bits]
    # for c in list_bits:

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
    
    # byte_list = textwrap.wrap(bits, 8)

    print('Imprimindo...')
    result.write(getbit_size.to_bytes(1, byteorder='big'))

    for i in range(math.ceil(len(bits) / 8)):
        byte = bits[i*8:i*8+8]

        byteorder = 'big'
        if len(byte) < 8:
            byte = '1' + byte

        result.write(int(byte, 2).to_bytes(1, byteorder))
    
    result.close()
    file.close()

    # if len(TEMP_FILE_BITS) < len(bits):
    #     TEMP_FILE_BITS = bits

    print('Compressao concluida!')
    return 1
