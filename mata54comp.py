import sys
from compressor import encoding
from descompressor import decoding

BITS = 2
MAX_BITS = 8

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