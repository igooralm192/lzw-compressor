import sys
from compressor import encoding
from descompressor import decoding

args = sys.argv[1:]

if len(args) != 2:
    exit(0)

[mode, file] = args

if mode == '-c':
    encoding(file)
elif mode == '-d':
    decoding(file)
else:
    exit(0)