import math, textwrap
from helper import byteToBin, fullByte, binToByte

def encoding(file_bits: str, tam_bits: int, max_bits: int, len_temp_file: int):
    bit_size = tam_bits+1
    max_size = (1 << tam_bits)
    # O dicionario é gerado
    dictionary = {}
    for i in range(max_size):
        dictionary[fullByte(bin(i)[2:], length=tam_bits)] = i

    prefix = ""
    codes = []
    index = max_size

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

            # Verifica se a tabela passou do limite
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
    
    # Encontra o maior valor da tabela usado para compressão e guarda o tamanho dos bits dele (getbit_size)
    for code in codes:
        max_code = max(code, max_code)
    getbit_size = len(bin(max_code)[2:])

    # Guarda os bits dos valores usados da tabela com um tamanho de getbit_size bits
    for code in codes:
        code_byte = fullByte(bin(code)[2:], length=getbit_size)
        bits += code_byte
    
    # Verifica se o .cmp seria maior que o original. Se sim, o .cmp guardará o arquivo original
    if len(bits) > len(file_bits):
        bits = file_bits
        getbit_size = len(bin(max_original_code)[2:])

    # Verifica se o .cmp gerado até então pelos testes é maior que o do teste atual. Se sim, os parametros são atualizados.
    # Vale lembrar que o .cmp final será o menor gerado pelos testes de compressão
    if len_temp_file > len(bits) or len_temp_file == 0:
        return True, [bits, fullByte(bin(tam_bits)[2:])[3:], fullByte(bin(max_bits)[2:])[3:], fullByte(bin(getbit_size)[2:])[3:]]
    else:
        return False, [None, None, None, None]
