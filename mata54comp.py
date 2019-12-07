# Trabalho 2 de EDA2 - Victor Pinheiro Aguiar Silva e Igor de Almeida Nascimento

import sys, math
from compressor import encoding
from descompressor import decoding
from helper import byteToBin, binToByte, fullByte, toInt

# Variaveis para guardar os bits do arquivo .cmp a ser gerado e os parametros
# descritos no relatorio para cada teste a ser feito na compressao
TEMP_FILE_BITS = ''
TEMP_TAM_BITS = ''
TEMP_MAX_BITS = ''
TEMP_GET_BIT_SIZE = ''

args = sys.argv[1:]

if len(args) != 2:
    exit(0)

[mode, filename] = args

if mode == '-c':
    min_range = 2
    max_range = 21
    
    file = open(filename, "rb")
    # O arquivo é aberto e todos seus bits guardados em file_bits
    file_bits = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        byte = byteToBin(byte, full=True)
        file_bits += byte
        
    for i in range(min_range, max_range):
        BITS = i
        MAX_BITS = min(i+i, 24)

        bits_to_temp, config = encoding(file_bits, BITS, MAX_BITS, len(TEMP_FILE_BITS))
        # A funcao de comprimir (encoding) retorna True e os parametros do teste atual se o arquivo .cmp
        # é menor que o original. False caso contrário.
        if (bits_to_temp):
            [TEMP_FILE_BITS, TEMP_TAM_BITS, TEMP_MAX_BITS, TEMP_GET_BIT_SIZE] = config

    file.close()
    result = open(filename.split('.')[0]+".cmp", "wb")

    # O arquivo .cmp é gerado com os parametros no inicio em 4 bytes 
    # (5 bits cada + 1 bit para saber se o ultimo byte é somente bits 0 + 8 bits pra quantidade de zeros a esquerda no ultimo byte 
    # + 8 bits pra saber se o arquivo foi realmente comprimido ou não)
    config = TEMP_TAM_BITS + TEMP_MAX_BITS + TEMP_GET_BIT_SIZE + '0'

    lastByte = math.ceil(len(TEMP_FILE_BITS) / 8) - 1
    byte = TEMP_FILE_BITS[lastByte*8:lastByte*8+8]
    last_byte_zero = False
    qnt_zero = 0
    
    if byte.find('1') == -1:
        last_byte_zero = True
        qnt_zero = len(byte)
        config = config[:len(config)-1] + '1'
    else:
        qnt_zero = byte.find('1')

    config += fullByte(bin(qnt_zero)[2:])
    if file_bits == TEMP_FILE_BITS:
        config += fullByte(bin(1)[2:])
    else:
        config += fullByte(bin(0)[2:])

    for i in range(4):
        byte = config[i*8:i*8+8]
        result.write(binToByte(byte))

    for i in range(math.ceil(len(TEMP_FILE_BITS) / 8)):
        byte = TEMP_FILE_BITS[i*8:i*8+8]
        byteorder = 'big'
        # if len(byte) < 8:
        #     byte = '1' + byte
        result.write(int(byte, 2).to_bytes(1, byteorder))

elif mode == '-d':
    decoding(filename)