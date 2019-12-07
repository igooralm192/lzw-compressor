import math
    
# Transformar um inteiro em byte
def toByte(n):
    return int.to_bytes(n, math.ceil(n/255), byteorder='big')

# Transformar uma sequencia de bits em inteiro
def toInt(binary, base=2):
    return int(binary, base)

# Transformar uma sequencia de bits em bytes
def binToByte(binary):
    return int(binary, 2).to_bytes(math.ceil(len(binary) / 8), byteorder='big')

# Transformar um byte em uma sequencia de bits, podendo completa-la até o tamanho de 8 bits se full == True
def byteToBin(byte, full=False):
    binary = bin(int.from_bytes(byte, byteorder='big'))[2:]
    if full:
        binary = fullByte(binary)
    return binary

# Completa a sequencia de bits "binary" até o tamanho length
def fullByte(binary, length=8):
    rest = length - len(binary)
    zeros = '0' * rest
    binary = zeros + binary
    return binary

def notFullByte(binary: str, length=0):
    if length != 0:
        return binary[-length:]

    firstBit1 = binary.find('1')
    return binary[firstBit1:]