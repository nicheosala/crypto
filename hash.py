from DES.DES_utils import xor


def get_blocks(binary_text: str, block_size: int):
    return (binary_text[i:i + block_size] for i in range[::block_size])


def hash(m: list[str], h, IV: str) -> str:
    '''
    @param m is a list of blocks of size 'block_size', already padded.
    @param h is the compression function, that receives two parameters as input.
    @param IV is the initial value for compression.
    '''
    from functools import reduce
    return reduce(h, m, IV)
    # --> h(h(h(IV, m[0]), m[1]), ...)


def DM(m, E, IV):
    '''
    Davies-Meyer scheme.

    @param E is the encryption funciton of a block cipher like DES.
    I assumed E takes the key as first parameter and the cleartext as second parameter.
    A lot of care must be put so that the bit length of the parameters is the same.
    '''
    def h(H, m): return xor(E(m, H), H)
    return hash(m, h, IV)


def MMO(m, E, IV):
    '''
    Matyas-Meyer-Oseas scheme.
    '''
    def h(H, m): return xor(E(H, m), H)
    return hash(m, h, IV)


def MP(m, E, IV):
    '''
    Miyaguchi-Preneel scheme.
    '''
    def h(H, m): return xor(xor(E(H, m), m), H)
    return hash(m, h, IV)


if __name__ == '__main__':
    m = ['1010', '1111']

    def h(prev, next): return ''.join(map(lambda x, y: str(
        int(x) ^ int(y)), prev, next))[:4]   # Toy compression function
    IV = '0000'
    print(hash(m, h, IV))
