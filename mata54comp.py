import sys, math, time
from compressor import encoding
from descompressor import decoding
from helper import byteToBin, binToByte

start_time = time.time()

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

    print('Analisando arquivo...')
    file_bits = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        byte = byteToBin(byte, full=True)
        file_bits += byte

    for i in range(min_range, max_range):
        print('Teste ', i)
        
        BITS = i
        MAX_BITS = min(i+i, 24)

        bits_to_temp, config = encoding(file_bits, BITS, MAX_BITS, len(TEMP_FILE_BITS))
        if (bits_to_temp):
            [TEMP_FILE_BITS, TEMP_TAM_BITS, TEMP_MAX_BITS, TEMP_GET_BIT_SIZE] = config
        print()

    file.close()
    result = open(filename.split('.')[0]+".cmp", "wb")

    print([int(TEMP_TAM_BITS, 2), int(TEMP_MAX_BITS, 2)])
    print('Imprimindo...')
    config = TEMP_TAM_BITS + TEMP_MAX_BITS + TEMP_GET_BIT_SIZE + '0'
    print(config)
    for i in range(2):
        byte = config[i*8:i*8+8]
        result.write(binToByte(byte))

    for i in range(math.ceil(len(TEMP_FILE_BITS) / 8)):
        byte = TEMP_FILE_BITS[i*8:i*8+8]

        byteorder = 'big'
        if len(byte) < 8:
            byte = '1' + byte

        result.write(int(byte, 2).to_bytes(1, byteorder))
    print('Compressao concluida!')
elif mode == '-d':
    decoding(filename)

end_time = time.time()
print("Total execution time: {}".format(end_time - start_time))