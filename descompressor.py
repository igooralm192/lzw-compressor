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

def toByte(n):
    return int.to_bytes(n, 1, byteorder='big')

def decoding(filename: str, tam_bytes: int):
    bit_size = 9
    max_size = (1 << bit_size) - 1
    dictionary = []
    for i in range(256):
        dictionary.append(ByteList(bytes([i]), value=i))

    file = open(filename, "rb")
    result = open(filename.split('.')[0], "wb")

    prefix = ByteList()
    codes = []
    index = 256

    i = 0

    c = file.read(tam_bytes)
    if c:
        c = int.from_bytes(c, "big")
        codes.append(bytes([c]))
        # print(c, ' - ', findValueOnDict(c, dictionary).getList())

    while True:
        # print(i, ' ', len(codes))
        if i >= len(codes): 
            c = file.read(tam_bytes)
            if c:
                c_int = int.from_bytes(c, 'big')
                find_c = findValueOnDict(c_int, dictionary)

                if find_c is None:
                    # print('find_c is None')
                    putDict = ByteList(*(prefix.getList()), prefix.getList()[0], value=index)
                    dictionary.append(putDict)

                    c = []
                    c += prefix.getList()
                    c.append(prefix.getList()[0])
                    # print(c_int, ' - ', c)
                    index += 1
                    codes += c
                    prefix = ByteList(codes[i])
                    i += 1
                else:                
                    # print(c_int, ' - ', findValueOnDict(c_int, dictionary).getList())
                    # print('find_c not None : ', find_c.getList())
                    # c = int.to_bytes(c_int, tam_bytes, byteorder='big')
                    # c = [toByte(item) for item in list(c)] 

                    codes += find_c.getList()
            else:
                break
            

        p = prefix+codes[i]
        # print('codes: ', codes)
        # print('prefix: ', prefix.getList())
        # print('p: ', p.getList())
        find_p = findOnDict(p.getList(), dictionary)

        if find_p != None:
            # print('find_p != None')
            prefix = find_p
        else:
            p.setValue(index)
            dictionary.append(p)
            # print('find_p == None : ', p.getList())

            index += 1

            if index == max_size:
                bit_size += 1

            if bit_size > tam_bytes*8:
                bit_size = 9
                index = 256
                dictionary = []
                for i in range(256):
                    dictionary.append(ByteList(bytes([i]), value=i))

            prefix = ByteList(codes[i])
        i += 1

    for code in codes:
        result.write(code)
    
    result.close()
    file.close()
    return 1