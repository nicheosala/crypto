from accessories import *
from math import ceil, sqrt


def discrete_log(base: int, argument: int, n: int, p: int) -> int:

    assert prime(p)         # may be relaxed?
    assert (p - 1) % n == 0  # may be relaxed?

    base %= p
    argument %= p

    assert coprime(base, p)
    assert coprime(argument, p)

    for x in range(p):
        if pow(base, x, p) == argument:
            return x % n

    raise ValueError('Discrete logarithm not found.')


def BSGS(base: int, argument: int, n: int, p: int) -> int:
    '''Baby Step Giant Step'''

    assert prime(p)         # may be relaxed?
    assert (p - 1) % n == 0  # may be relaxed?

    base %= p
    argument %= p

    assert coprime(base, p)
    assert coprime(argument, p)

    m = ceil(sqrt(n))
    table = dict((pow(base, j, p), j) for j in range(m + 1))
    y = argument
    g_m = pow(base, -m, p)
    for i in range(m + 1):
        if y in table:
            return (i * m + table[y]) % n
        y = y * g_m % p

    raise ValueError('Discrete logarithm not found.')

# TODO does not work
def pollard_ρ(base: int, argument: int, n: int, p: int) -> int:
    S1, S2, S3 = range(1, p // 3 + 1), range(p // 3 + 1, (p *
                                         2) // 3 + 1), range((p * 2) // 3 + 1, p)

    def f(a, b, x):
        if x in S1:
            return a % n, (b + 1) % n, (argument * x) % p
        if x in S2:
            return (2 * a) % n, (2 * b) % n, pow(x, 2, p)
        if x in S3:
            return (a + 1) % n, b % n, (base * x) % p

    a, b, x = 0, 0, 1
    da, db, dx = 0, 0, 1
    print('x\ta\tb\t\tdx\tda\tdb')

    while True:
        a, b, x = f(a, b, x)
        da, db, dx = f(*f(da, db, dx))
        print(f'{x}\t{a}\t{b}\t\t{dx}\t{da}\t{db}')
        if b == db:
            raise Exception('Cycle detected')
        if x == dx:
            return ((a - da) * inverse(db - b, n)) % n


def PH(base: int, argument: int, n: int, p: int) -> int:
    '''Pohlig - Hellman discrete logarithm computation.'''

    assert prime(p)         # may be relaxed?
    assert (p - 1) % n == 0  # may be relaxed?

    base %= p
    argument %= p

    assert coprime(base, p)
    assert coprime(argument, p)

    fs = [(k, v) for k, v in prime_factors_mult(n).items()]
    s = len(fs)
    system = []

    for i in range(s):
        l = []
        p_i, e_i = fs[i]
        γ, η = 1, pow(base, n // p_i, p)
        for j in range(e_i):
            if j > 0:
                γ = γ * pow(base, l[j - 1] * p_i ** (j - 1), p) % p
            δ = pow(argument * inverse(γ, p), n // (p_i ** (j + 1)), p)
            # print(f'η: {η}, γ: {γ}, δ: {δ}, l: {l}')
            l.append(BSGS(η, δ, p_i, p))
        x = sum(l[k] * p_i ** k for k in range(e_i)) % p
        system.append((x, p_i ** e_i))

    return CRT(*system)[0]


if __name__ == '__main__':
    #print(BSGS(2, 3, 31))
    # print(pollard_ρ(2, 3, 31, 30))  # TODO does not work
    #print(pollard_ρ(122, 64, 607, 101))
    assert discrete_log(250, 250, 2, 251) == BSGS(250, 250, 2, 251)
    assert discrete_log(20, 149, 5, 251) == BSGS(20, 149, 5, 251)
    assert discrete_log(71, 210, 250, 251) == BSGS(71, 210, 250, 251)

    assert discrete_log(250, 250, 2, 251) == PH(250, 250, 2, 251)
    assert discrete_log(20, 149, 5, 251) == PH(20, 149, 5, 251)
    assert discrete_log(71, 210, 250, 251) == PH(71, 210, 250, 251)

    print(pollard_ρ(64, 122, 101, 607))