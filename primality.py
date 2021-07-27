from itertools import takewhile
from random import randint

from accessories import *


def fermat(n: int, k: int) -> tuple[bool, float]:

    assert k in range(1, n)

    if n == 2:
        return True, 1
    
    if n <= 1 or n % 2 == 0:
        return False, 1

    for _ in range(k):
        a = randint(2, n - 1)
        if pow(a, n - 1, n) != 1:
            return False, 1

    return True, 1 - pow(2, -k)


def MR_params(n):
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return d, s


def MR(n: int, k: int) -> tuple[bool, float]:
    '''Miller - Rabin primality test.'''
    if n == 2:
        return True, 1
    
    if n <= 1 or n % 2 == 0:
        return False, 1

    d, s = MR_params(n)

    for _ in range(k):
        a = randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(1, s):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False, 1

    return True, 1 - pow(4, -k)

def test(primality_test):
        LIMIT = 10 ** 5
        fp, fn, tp, tn = 0, 0, 0, 0
        ps = set(takewhile(lambda x : x < LIMIT, primes()))
        for p in range(21, LIMIT):
            is_prime, maybe_prime = p in ps, primality_test(p)
            if is_prime and maybe_prime:
                tp += 1
            elif not is_prime and not maybe_prime:
                tn += 1
            elif is_prime and not maybe_prime:
                print(f'false positive! {p}')
                fn += 1
            else:
                print(f'false positive! {p}')
                fp += 1
        print(f'True positive: {tp}\nTrue negative: {tn}\nFalse positive: {fp}\nFalse negative: {fn}')

if __name__ == '__main__':

    print("Miller - Rabin primality test")
    MR_primality_test = lambda p: MR(p, 10)[0]
    test(MR_primality_test)

    print("Fermat primality test")
    fermat_primality_test = lambda p: fermat(p, 10)[0]
    test(fermat_primality_test)

    

    