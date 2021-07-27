'''
Nicolò Sala, 2nd July 2021

I implemented these functions studying for an exam.
These implementations are not supposed to be the most efficient possible.
My intention is to work on them and try to do all my best in order to optimize
them, while keeping clean code.
'''
from math import sqrt, floor, prod
from typing import Iterator
from numpy import array
from functools import reduce, partial
from itertools import count


def EEA(a: int, b: int) -> tuple[int, int, int]:
    '''Extended Euclidean Algorithm'''
    u = array([abs(a), 1, 0])
    v = array([abs(b), 0, 1])

    while v[0] != 0:
        u, v = v, u - (u[0] // v[0]) * v

    return int(u[0]), int(u[1]), int(u[2])


def GCD(a: int, b: int) -> int:
    '''
    Greatest Common Divisor

    The Greatest Common Divisor between two integer numbers
    is the greatest natural number that is divisor of both of them.

    We assume GCD(0, 0) == 0 based on:
    https://math.stackexchange.com/questions/495119/what-is-gcd0-0
    '''
    return EEA(a, b)[0]


def coprime(a: int, b: int) -> bool:
    '''CHECKED
    Two integer numbers are coprime if and only if their
    Common Greatest Divisor is equal to 1.
    '''
    return GCD(a, b) == 1


def coprimes(n: int, start: int = 0) -> Iterator[int]:
    '''
    Return all and only the integer numbers coprime with the integer number n,
    starting from the integer number :start, included.
    '''
    return filter(partial(coprime, a=n), range(start, n))


def totient(n: int) -> int:
    '''
    Return the totient of the positive integer number n.

    The totient of a positive integer number n can be defined as the count of
    numbers in [1, n) coprimes with n.

    Otherwise, it can be demonstrated the totient of n is the productory of
    n divided by f and multiplied by f - 1, where f is a prime factor of n.

    The 'definition method' has a time complexity of O(n).
    The 'prime factors method' has a time complexity dependent from the
    complexity of factorizing n, that can be easily less than O(n) (typically
    O(sqrt(n)) or smaller).
    BUT, after computing the prime factors, you also have to reduce them all.
    This reduction MAY have non-constant time cost. So, I don't know which
    method is best.
    '''
    assert n > 0, "The totient is only defined for positive integer numbers."
    return reduce(lambda acc, f: (acc // f) * (f - 1), prime_factors(n), n)
    # return len(tuple(coprimes(n)))


def divisor(x: int, n: int) -> bool:
    '''CHECKED
    Return True if the integer number x is a divisor of the
    integer number n, otherwise False.

    The integer number x is a divisor of the integer number n if and only if
    there exists an integer number a such that x * a == n.

    This is equivalent to say that:
    The integer number x is a divisor of the integer number n if and only if:
    - when x == 0, also n == 0;
    - when x != 0, then n / x == a + 0, where a is any integer number,
    that is n % x == 0

    Notice that every integer number is a divisor of 0.
    Notice that 0 is a divisor only of 0 itself.
    '''
    return (x == 0 and n == 0) or (x != 0 and n % x == 0)


def natural_divisors(n: int) -> Iterator[int]:
    '''CHECKED
    Return all and only the *natural* divisors of the integer number n.

    Notice that any natural number is a divisor of 0.
    '''
    return count() if n == 0 else filter(partial(divisor, n=n), range(n + 1))


def proper_natural_divisors(n: int) -> Iterator[int]:
    '''CHECKED
    Return all and only the proper *natural* divisors of n.

    A proper natural divisor of an integer number n is a natural divisor
    different from n.

    In doubt, I assumed the proper divisors of 0 are all the natural number
    except 0 itself.
    '''
    return filter(lambda d: d != n, natural_divisors(n))


def prime_factors_mult(n: int) -> dict[int, int]:
    result: dict = {}
    for p in primes():
        if n <= 1:
            break
        if divisor(p, n):
            result[p] = 0
            while divisor(p, n):
                result[p] += 1
                n //= p
    return result


def prime_factors(n: int) -> Iterator[int]:
    # VERY SLOW: return filter(prime, proper_factors(n))
    for p in primes():
        if n <= 1:
            break
        if divisor(p, n):
            yield p
            while divisor(p, n):
                n //= p


def prime(n: int) -> bool:
    '''Trivial deterministic primality test.'''
    return n > 1 and all(not divisor(i, n) for i in range(2, floor(sqrt(n))+1))


def primes() -> Iterator[int]:
    '''Return all the prime numbers.'''
    return filter(prime, count())


def composite(n: int) -> bool:
    return n > 1 and not prime(n)


def charmichael(n: int) -> bool:
    return composite(n) and all(pow(a, n - 1, n) == 1 for a in coprimes(n))


def charmichaels() -> Iterator[int]:
    '''Return all the Charmichael's numbers.'''
    return filter(charmichael, count())


def inverse(x: int, p: int) -> int:

    # Using Extended Euclidean algorithm:
    return EEA(x, p)[1]

    # Using Fermat's theorem:
    # return SM(x, p - 2, p)


def B_smooth(B: int, n: int) -> bool:
    return all(f < B for f in prime_factors(n))


def B_power_smooth(B: int, n: int) -> bool:
    return all(f ** p < B for (f, p) in prime_factors_mult(n).items())


def SM(base: int, exp: int, mod: int) -> int:
    '''Square & multiply.'''
    def square(x): return pow(x, 2, mod)
    def multiply(x, bit): return (x * (base if bit == '1' else 1)) % mod
    def sq_mul(x, bit): return multiply(square(x), bit)

    return reduce(sq_mul, bin(exp)[2:], 1)


def CRT(*eqs: tuple[int, int]) -> tuple[int, int]:
    '''
    Chinese Remainder Theorem.
    https://crypto.stanford.edu/pbc/notes/numbertheory/crt.html

    x = a[i] (mod m[i])
    @param eqs contains tuples of two integers:
    - the first integer is 'a[i]'
    - the second integer is 'm[i]'

    TODO check couples of M[i] are all coprime (hypothesis of the theorem).
    '''
    # TODO assert all(lambda t: coprime(t[0], t[1]), combinations(moduli, 2))

    M = prod(eq[1] for eq in eqs)
    return sum(a * (M // m) * inverse(M // m, m) for (a, m) in eqs) % M, M


def random_integer(min, max, condition=True):
    '''Very bad performance. Look for something else.'''
    from random import choice
    return choice(tuple(filter(condition, range(min, max))))


def random_prime(min, max):
    return random_integer(min, max, prime)


def random_coprime(n, min, max):
    return random_integer(min, max, partial(coprime, b=n))


def pick_distinct_primes(n: int, min: int, max: int) -> tuple[int, ...]:
    primes: set = set()

    while len(primes) < n:
        primes.add(random_prime(min, max))

    return tuple(primes)


if __name__ == '__main__':
    pass
