import sys
from compressor import encoding
from descompressor import decoding

BYTES = 3

args = sys.argv[1:]

if len(args) != 2:
    exit(0)

[mode, file] = args

if mode == '-c':
    encoding(file, BYTES)
elif mode == '-d':
    decoding(file, BYTES)
else:
    exit(0)