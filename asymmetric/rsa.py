from accessories import *


def pick_random_prime_couple(min=1, max=1000) -> tuple[int, int]:
    '''
    Get two distinct prime numbers, p and q.
    '''
    p = random_prime(min, max)
    q = random_prime(min, max)

    while q == p:
        q = random_prime(min, max)

    return p, q


def pick_public_exp(phi):
    DEFAULT = 2 ** 16 + 1
    if coprime(DEFAULT, phi):
        return DEFAULT
    else:
        return random_coprime(phi, 2, phi - 1)


def rsa_encrypt(m, e, n):
    return pow(m, e, n)


def rsa_decrypt(c, d, p, q):
    return pow(c, d, p * q)
    # Speedup (for big numbers?), using Chinese Remainder Theorem:
    # return CRT((pow(c, d, p), p), (pow(c, d, q), q))[0]


def rsa_decrypt_bruteforce(c, e, n):

    # Nota bene: il seguente tentativo di fattorizzazione è il cuore della
    # sicurezza di RSA. Se questa operazione fosse possibile anche per numeri
    # giganteschi, allora RSA non sarebbe un algoritmo sicuro.
    _, p, q = tuple(proper_natural_divisors(n)) # Discard the trivial proper divisor 1.

    assert prime(p) and prime(q)

    phi_n = (p - 1) * (q - 1)
    d = inverse(e, phi_n)

    return rsa_decrypt(c, d, p, q)


def factorize_n_knowing_d(d: int, e: int, n: int) -> tuple[int, int]:
    '''
    Statement: knowing the private exponent d corresponding to the public key (n, e),
    it is possible to efficiently factor n.
    '''
    for x in coprimes(n, start=2):
        exp = (e * d - 1) >> 1  # (e * d - 1) // 2
        y = pow(x, exp, n)
        while y == 1:
            exp = exp >> 1
            y = pow(x, exp, n)
        if y != -1:
            p = GCD(y - 1, n)
            break

    return (p, n // p)


def factorize_n_knowing_phi(phi: int, n: int) -> tuple[int, int]:
    '''
    Statement: knowing the totient phi(n) corresponding to the public key (n, e),
    it is possible to efficiently factor n.
    '''
    b = (1 + n - phi) // 2
    delta = floor(sqrt(b ** 2 - n))

    return b + delta, b - delta


def retrieve_m_same_n(c1, c2, e1, e2, n):
    '''
    Statement: Given two RSA ciphertexts c1 = Enc(n,e1)(m), c2 = Enc(n,e2)(m), one can
    easily recover the original message m if gcd(e1, e2) = 1.

    Interesting: this attack finds the plaintext message without factorizing n.
    This is an evidence that breaking RSA is easier than factoring.
    '''
    assert coprime(e1, e2), 'e1 and e2 must be coprime.'

    _, t1, t2 = EEA(e1, e2)

    return (pow(c1, t1, n) * pow(c2, t2, n)) % n


def retrieve_m_small_e(e, *eqs):
    '''
    Statement: The use of a small public exponent is unsafe in case multicast
    communications take place.

    Interesting: this attack finds the plaintext message without factorizing n.
    This is an evidence that breaking RSA is easier than factoring.
    '''
    return round(CRT(*eqs)[0] ** (1/e))


def OAEP():
    '''
    Optimized Asymmetric Encryption Padding.

    TODO
    '''
    pass


if __name__ == '__main__':

    # 1. Si scelgono a caso due numeri primi, p e q.
    p, q = pick_random_prime_couple()
    print("p:", p)
    print("q:", q)

    # 2. Si calcola il loro prodotto n, chiamato 'modulo'.
    n = p * q
    print("n:", n)

    # 3. Si calcola il prodotto phi(n) = (p - 1) * (q - 1).
    phi_n = (p - 1) * (q - 1)
    print("phi(n):", phi_n)

    # 4. Si sceglie poi un numero e, chiamato 'esponente pubblico', coprimo
    # con phi_n e più piccolo di phi_n
    e = pick_public_exp(phi_n)
    print("e:", e)

    # 5. Si calcola il numero d, chiamato esponente privato, tale che
    # il suo prodotto con e sia congruo a 1 modulo 𝜑(𝑛)
    d = inverse(e, phi_n)
    print("d:", d)

    print("Public key (n, e):", (n, e))
    print("Private key (n, d):", (n, d))

    plaintext = 346788
    print("Plaintext:", plaintext)

    ciphertext = rsa_encrypt(plaintext, e, n)
    print("Encrypted text:", ciphertext)

    decrypted = rsa_decrypt(ciphertext, d, p, q)
    print("Decrypted text:", decrypted)

    brute_force_decrypted = rsa_decrypt_bruteforce(ciphertext, e, n)
    print("Brute-force decrypted text:", brute_force_decrypted)

    # The following examples are taken from pg. 174 of
    # 'Cryptography: an introduction (3rd edition)'
    p, q = factorize_n_knowing_d(507905, 17, 1441499)
    assert p == 1423 and q == 1013

    p, q = factorize_n_knowing_phi(18648, 18923)
    assert p == 149 and q == 127

    m = retrieve_m_same_n(1514, 8189, 11, 5, 18923)
    assert m == 100

    m = retrieve_m_small_e(3, (50, 323), (268, 299), (1, 341))
    assert m == 67

    # TODO this does not work: incorrect m value
    # m = 67
    # e = 5
    # primes = pick_distinct_primes(e * 2, 1, 1000)
    # eqs =[]
    # for i in range(0, len(primes), 2):
    #     print(f'p: {primes[i]}, q: {primes[i + 1]}, n: {primes[i] * primes[i + 1]}')
    #     n = primes[i] * primes[i + 1]
    #     eqs.append((rsa_encrypt(m, e, n), n))
    # print(eqs)
    # m = retrieve_m_small_e(e, *eqs)
    # print(m)

