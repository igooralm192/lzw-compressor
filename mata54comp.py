import sys
from compressor import encoding
from descompressor import decoding

TEMP_FILE_BITS = ''

min_range = 2
max_range = 21
for i in range(min_range, max_range):
    print('Teste ', i)
    BITS = i
    MAX_BITS = i+i

    args = sys.argv[1:]

    if len(args) != 2:
        exit(0)

    [mode, file] = args

    if mode == '-c':
        encoding(file, BITS, MAX_BITS)
    elif mode == '-d':
        decoding(file, BITS, MAX_BITS)
    else:
        exit(0)
    print()