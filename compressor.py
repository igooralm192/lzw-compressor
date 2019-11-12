import math
from bytelist import ByteList

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

def encoding(filename: str, tam_bytes: int):
    bit_size = 9
    max_size = (1 << bit_size) - 1
    dictionary = []
    for i in range(256):
        dictionary.append(ByteList(bytes([i]), value=i))
    
    
    file = open(filename, "rb")
    result = open(filename.split('.')[0]+".cmp", "wb")
    
    prefix = ByteList()
    codes = []
    index = 256

    while True:
        c = file.read(1)
        # print(c)
        if not c:
            break

        p = prefix + c

        find_p = findOnDict(p.getList(), dictionary)
        if find_p != None:
            prefix = find_p
        else:
            codes.append(prefix.getValue())
            p.setValue(index)
            dictionary.append(p)
            index += 1

            if index == max_size:
                bit_size += 1

            if bit_size > tam_bytes*8:
                bit_size = 9
                index = 256
                dictionary = []
                for i in range(256):
                    dictionary.append(ByteList(bytes([i]), value=i))

            prefix = findOnDict([c], dictionary)
    
    codes.append(prefix.getValue())

    for code in codes:
        # print(findValueOnDict(code, dictionary).getList())
        # print(code, ' - ', findValueOnDict(code, dictionary).getList())
        result.write(code.to_bytes(tam_bytes, 'big'))
    
    result.close()
    file.close()
    return 1