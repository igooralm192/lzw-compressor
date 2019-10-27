
def encoding(filename: str):
    bit_size = 9
    max_size = (1 << bit_size) - 1
    dictionary = {}
    for i in range(256):
        dictionary[chr(i)] = i
    
    
    file = open(filename, "r")
    result = open(filename.split('.')[0]+".cmp", "wb")
    
    prefix = ""
    codes = []
    index = 256

    while True:
        c = file.read(1)
        if not c:
            break
        
        p = prefix+c

        if p in dictionary:
            prefix = p
        else:
            codes.append(dictionary[prefix])
            dictionary[p] = index
            index += 1

            if index == max_size:
                bit_size += 1

            prefix = c
    
    codes.append(dictionary[prefix])

    #print(dictionary, index, codes)

    for code in codes:
        result.write(code.to_bytes((bit_size%8)+1,'big'))
    
    result.close()
    file.close()
    return 1