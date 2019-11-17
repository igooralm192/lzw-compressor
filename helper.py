import math
    
def toByte(n):
    return int.to_bytes(n, math.ceil(n/255), byteorder='big')

def toInt(binary, base=2):
    return int(binary, base)

def binToByte(binary):
    return int(binary, 2).to_bytes(math.ceil(len(binary) / 8), byteorder='big')

def byteToBin(byte, full=False):
    binary = bin(int.from_bytes(byte, byteorder='big'))[2:]
    if full:
        binary = fullByte(binary)
    return binary

def fullByte(binary, length=8):
    rest = length - len(binary)
    zeros = '0' * rest
    binary = zeros + binary
    return binary