import math

def findOnDict(bytelist, array):
    for elem in array:
        if elem.getList() == bytelist:
            return elem
    return None

def findValueOnDict(integer, array):
    for elem in array:
        if elem.getValue() == integer:
            return elem
    return None
    
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

def fullByte(binary, reverse=False, length=8):
    rest = length - len(binary)
    if reverse:
        for i in range(rest):        
            binary += '0'
    else:
        for i in range(rest):
            binary = '0' + binary
    return binary

class ByteList:
    def __init__(self, *bytelist, value=None):
        self.value = value
        self.list = []
        for byte in bytelist:
            self.list.append(byte)

    def add(self, byte):
        self.list.append(byte)

    def __add__(self, byte):
        return ByteList(*self.list, byte, value=self.value)

    def setList(self, bytelist):
        self.list = bytelist

    def getList(self):
        return self.list

    def hasValue(self):
        return value != None

    def setValue(self, v):
        self.value = v

    def getValue(self):
        return self.value