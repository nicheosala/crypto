from random import *
from accessories import *


def get_public_params() -> tuple[int, int]:
    '''
    Return a generator g of a multiplicative subgroup of a finite
    field with prime order p. p is such that there exist two prime
    numbers p1 and p2: p == 2 * p1 * p2 + 1
    '''
    p1, p2 = pick_distinct_primes(2, 1, 100)
    p = 2 * p1 * p2 + 1

    while not (prime(p) and p1 != p2):
        p2 = random_prime(1, 100)
        p = 2 * p1 * p2 + 1

    # print(f'p1: {p1}, p2: {p2}, p: {p}')
    alfa = next(primitive_elements(p))

    return pow(alfa, (p - 1) // p1, p), p


def keygen(g: int, p: int) -> tuple[int, int]:
    from random import randint

    priv = randint(2, p - 1)
    # print(f'priv: {priv}, pub: {pow(g, priv, p)}')

    return priv, pow(g, priv, p)


def DH_key_exchange():
    '''Diffie - Hellman key exchange protocol.'''
    g, p = get_public_params()

    k_priv_a, k_pub_a = keygen(g, p)
    k_priv_b, k_pub_b = keygen(g, p)

    k_ab = pow(k_pub_a, k_priv_b, p)
    k_ba = pow(k_pub_b, k_priv_a, p)

    assert k_ab == k_ba


def EG_encrypt(m: int, p: int, g: int, g_s: int) -> int:
    '''El Gamal encryption.'''
    l = randint(0, p - 1)
    return pow(g, l, p), (m * pow(g_s, l, p)) % p


def EG_decrypt(gamma: int, delta: int, p: int, s: int) -> int:
    '''El Gamal decryption.'''
    return (pow(gamma, p - s - 1, p) * delta) % p


def EG_cryptoscheme():
    '''
    El Gamal protocol public key cryptoscheme.

    Based on original paper:
    https://caislab.kaist.ac.kr/lecture/2010/spring/cs548/basic/B02.pdf

    paper --> my notation:
    m       --> m
    p       --> p
    k       --> l
    alfa    --> g
    xa      --> s
    yb      --> g_s
    c1      --> gamma
    c2      --> delta
    K       --> g_s ** l
    '''
    g, p = get_public_params()
    s = randint(0, p - 1)   # TODO maybe s can be any integer number.

    m = randint(0, p - 1)
    assert m in range(p)

    gamma, delta = EG_encrypt(m, p, g, pow(g, s, p))
    # print(f'm: {m}, p: {p}, g: {g}, g ** s: {pow(g, s, p)}')
    # print(f'gamma: {gamma}, delta: {delta}')
    cleartext = EG_decrypt(gamma, delta, p, s)

    assert m == cleartext


def EG_signature_scheme():
    '''
    El Gamal signature scheme.

        Based on original paper:
    https://caislab.kaist.ac.kr/lecture/2010/spring/cs548/basic/B02.pdf

    paper --> my notation:
    m       --> m
    p       --> p
    k       --> l
    alfa    --> g
    xa      --> s
    r       --> gamma
    s       --> delta
    '''
    g, p = get_public_params()

    m = bin(randint(0, p - 1))[2:]
    assert int(m, 2) in range(p)

    s = randint(0, p - 1)
    g_s = pow(g, s, p)

    def h(m): return int(m, 2)  # toy hash function
    gamma, delta = EG_sign(m, p, g, s, h)
    EG_validate(m, p, g, g_s, h, gamma, delta)


def EG_sign(m, p, g, s, h):
    # Notice that l must be coprime. This is not required for l in the cryptoscheme.
    l = random_coprime(p - 1, 2, p - 1)
    gamma = pow(g, l, p)
    delta = inverse(l, p - 1) * (h(m) - s * gamma) % (p - 1)
    # print(f'gamma: {gamma}, delta: {delta}')
    return gamma, delta


def EG_validate(m, p, g, g_s, h, gamma, delta):
    assert pow(g_s, gamma, p) * pow(gamma, delta, p) % p == pow(g, h(m), p)


def get_public_dsa_params():
    '''
    Questa funzione cerca di portare a termine
    un compito difficilissimo.
    '''
    # p = random_prime(10 ** 6, 10 ** 7)
    # q = random_prime(1, 10 ** 6)

    # while not (p - 1) % q == 0:
    #     q = random_prime(1, 10 ** 6)
    p, q = 11, 5    # TODO find something more efficient
    # for the above lines of code.

    # print(f'p: {p}, q: {q}')
    pe = primitive_elements(p)
    alfa = next(pe)
    g = pow(alfa, (p - 1) // q, p)
    while g == 1:
        alfa = next(pe)
        g = pow(alfa, (p - 1) // q, p)

    return g, p, q


def DSA():
    '''Digital Signature Algorithm.'''
    g, p, q = get_public_dsa_params()
    s = random_coprime(q, 2, q)
    m = '0' # funziona solo così... 
    def h(m): return int(m, 2) % q # toy hash function
    gamma, delta = DSA_sign(m, p, q, g, s, h)
    DSA_validate(m, p, q, g, pow(g, s, p), h, gamma, delta)


def DSA_sign(m, p, q, g, s, h):

    delta = 0

    while delta == 0:

        l = random_coprime(q, 1, q)
        gamma = pow(g, l, p) % q

        while gamma == 0:
            l = random_coprime(q, 1, q)
            gamma = pow(g, l, p) % q

        delta = inverse(l, q) * (h(m) + s * gamma) % q
        # print(f'gamma: {gamma}, delta: {delta}')

    return gamma, delta


def DSA_validate(m, p, q, g, g_s, h, gamma, delta):

    if gamma not in range(1, q) or delta not in range(1, q):
        raise ValueError

    u1 = (h(m) * inverse(delta, q)) % q
    u2 = (gamma * inverse(delta, q)) % q

    assert (pow(g, u1, p) * pow(g_s, u2, p)) % q == gamma


if __name__ == '__main__':
    DH_key_exchange()
    EG_cryptoscheme()
    EG_signature_scheme()
    DSA()   # Non funziona bene
