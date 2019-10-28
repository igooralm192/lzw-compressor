def decoding(filename: str):
    bit_size = 9
    max_size = (1 << bit_size) - 1
    dictionary = {}
    for i in range(256):
        dictionary[i] = chr(i)

    file = open(filename, "rb")
    result = open(filename.split('.')[0], "w")

    prefix = ""
    chars = ""
    index = 256

    i = 0

    c = file.read(2)
    if c:
        c_bytes = int.from_bytes(c, "big")
        c = dictionary[c_bytes]
        chars += c

    while True:
        if (i >= len(chars)):
            c = file.read(2)
            if c:
                c_bytes = int.from_bytes(c, "big")
                if c_bytes not in dictionary:
                    dictionary[index] = prefix + prefix[0]
                    c = dictionary[index]
                    
                    index += 1
                    chars += c
                    prefix = chars[i]
                    i += 1
                else:
                    c = dictionary[c_bytes]
                    chars += c
            else:
                break

        p = prefix+chars[i]

        if p in dictionary.values():
            prefix = p
        else:
            dictionary[index] = p

            index += 1

            if index == max_size:
                bit_size += 1

            prefix = chars[i]
        
        i += 1

    for char in chars:
        result.write(char)
        # print(char, end='')
    
    result.close()
    file.close()
    return 1