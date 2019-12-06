from helper import fullByte, toInt, binToByte, toByte, byteToBin
import textwrap

def decoding(filename: str):
    file = open(filename, "rb")
    result = open(filename.split('.')[0], "wb")

    # Resgata os parametros descritos no relatório com os 2 primeiros bytes do .cmp
    config_byte_1 = byteToBin(file.read(1), full=True)
    config_byte_2 = byteToBin(file.read(1), full=True)
    config_byte_3 = byteToBin(file.read(1), full=True)

    tam_bits = toInt(config_byte_1[:5])
    max_bits = toInt(config_byte_1[5:] + config_byte_2[:2])
    getbit_size = toInt(config_byte_2[2:7])

    last_byte_zero = False
    qnt_zero = 0
    if config_byte_2[-1:] == '1':
        last_byte_zero = True
        qnt_zero = toInt(config_byte_3)

    bit_size = tam_bits+1
    max_size = (1 << tam_bits)

    # Gera um dicionario (tabela) para mapear um valor para uma lista de sequencia de bits
    # Gera um dicionario (tabela) para mapear uma sequencia de bits em um valor
    dictionary = {}
    rev_dict = {}
    for i in range(max_size):
        dictionary[i] = [fullByte(bin(i)[2:], length=tam_bits)]
        rev_dict[fullByte(bin(i)[2:], length=tam_bits)] = i

    # Lê o arquivo .cmp e coloca seus bits em file_bits
    file_bits = ''
    origin_byte = ''
    while True:
        byte = file.read(1)
        if not byte:
            break
        
        byte = bin(int.from_bytes(byte, byteorder="big"))[2:]
        origin_byte = byte
        byte = fullByte(byte)
        file_bits += byte

    if last_byte_zero:
        zeros = '0' * qnt_zero
        file_bits = file_bits[:len(file_bits)-8] + zeros

    import math
    byte_file = []
    for i in range(math.ceil(len(file_bits) / getbit_size)):
        byte_file.append(file_bits[i*getbit_size:i*getbit_size+getbit_size])

    prefix = []
    codes = []
    index = max_size
    c = []
    i = 0
    index_file = 0

    if index_file < len(byte_file):
        c = byte_file[index_file]
        index_file += 1
        c = dictionary[toInt(c)]
        codes += c

    while True:
        if (i >= len(codes)):
            if index_file < len(byte_file):
                c = byte_file[index_file]

                index_file += 1
                c = toByte(int(c, 2))

                c_int = int.from_bytes(c, 'big')

                if c_int not in dictionary:
                    dictionary[index] = prefix + [prefix[0]]
                    c = dictionary[index]
                    rev_dict[''.join(dictionary[index])] = index
                    
                    index += 1
                    codes += c
                    prefix = [codes[i]]
                    i += 1
                else:
                    c = dictionary[c_int]
                    codes += c
            else:
                break

        p = prefix
        p.append(codes[i])

        if ''.join(p) in rev_dict:
            prefix = p
        else:
            dictionary[index] = p
            rev_dict[''.join(p)] = index

            index += 1

            if index == max_size:
                bit_size += 1

            # Verifica se as tabelas passaram do limite
            if bit_size > max_bits:
                bit_size = tam_bits+1
                dictionary = {}
                rev_dict = {}
                for i in range(max_size):
                    dictionary[i] = [fullByte(bin(i)[2:], length=tam_bits)]
                    rev_dict[fullByte(bin(i)[2:], length=tam_bits)] = i
                index = max_size

            prefix = [codes[i]]
        
        i += 1

    
    codes = ''.join(codes)

    # Verifica se o arquivo descomprimido seria maior que o original. Se sim, significa que no .cmp está guardado o 
    # arquivo original e esse é escrito novamente no novo arquivo gerado pela descompressão
    if len(codes) < len(file_bits):
        codes = file_bits

    # Escreve o arquivo descomprimido de byte em byte
    import math

    for i in range(math.ceil(len(codes) / 8)):
        code = codes[i*8:i*8+8]
        result.write(binToByte(code))

    result.close()
    file.close()
    return 1