from DES import shift_left, xor


def get_blocks(binary_text: str, block_size: int):
    return (binary_text[i:i + block_size] for i in range[::block_size])


def ECB_encrypt(binary_text: str, E: function, block_size: int):
    '''
    Electronic Code Book
    '''
    m = get_blocks(binary_text, block_size)
    c = map(E, m)

    return tuple(c)


def CBC_encrypt(binary_text: str, E: function, block_size: int, IV):
    '''
    Cipher Block Chaining
    '''
    m = get_blocks(binary_text, block_size)

    c = [IV]

    for i in range(1, len(m)):
        c.append(E(xor(m[i], c[i - 1])))

    return tuple(c[1:])


def CBC_decrypt(binary_text: str, D: function, block_size: int, IV):
    '''
    Cipher Block Chaining
    '''
    c = get_blocks(binary_text, block_size)

    m = [IV]

    for i in range(1, len(c)):
        m.append(xor(D(c[i]), c[i - 1]))

    return tuple(m[1:])


def CFB_encrypt(binary_text: str, E: function, block_size: int, IV, J):
    '''
    Cipher feedback mode
    '''
    m = get_blocks(binary_text, block_size)

    ISR = IV
    c = []

    for i in range(len(m)):
        OSR = E(ISR)
        c.append(xor(m[i], OSR[J]))
        ISR = xor(shift_left(ISR, J), c[i])  # sure?

    return tuple(c)


def OFB_encrypt(binary_text: str, E: function, block_size: int, IV, J):
    '''
    Cipher feedback mode
    '''
    m = get_blocks(binary_text, block_size)

    ISR = [IV]
    c = []

    for i in range(1, len(m)):
        OSR = E(ISR)
        c.append(xor(m[i], OSR[J]))
        ISR = xor(shift_left(ISR, J), OSR[J])  # sure?

    return tuple(c)


def CTR_encrypt(binary_text: str, E: function, block_size: int, IV):
    '''
    CounTeR mode
    '''
    m = get_blocks(binary_text, block_size)

    ctr, c = IV, []

    for i in range(len(m)):
        ctr += 1
        t = E(ctr)
        c.append(xor(m[i], t))

    return tuple(c)
