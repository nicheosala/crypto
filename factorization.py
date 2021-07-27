from random import randint
from accessories import GCD
from math import ceil, sqrt, floor


def trivial(n: int) -> tuple[int, int]:
    '''
    Trivial factoring method.
    '''
    for i in range(2, ceil(sqrt(n))):
        if n % i == 0:
            return i, n // i


def fermat(n: int) -> tuple[int, int]:
    '''
    Fermat's factoring method.
    '''
    if n % 2 == 0:
        return n // 2, 2

    x: int = ceil(sqrt(n))
    y_squared: int = x ** 2 - n
    # print(f'x: {x}, y: {y_squared}')

    while not sqrt(y_squared).is_integer():
        y_squared += 2 * x + 1
        x += 1
        # print(f'x: {x}, y: {y_squared}')

    y = floor(sqrt(y_squared))
    return x - y, x + y


def pollard_ρ(n: int) -> int:
    '''
    Pollard's ρ factoring method.
    '''
    def f(x): return (x ** 2 + 1) % n

    x = randint(1, n - 1)
    y = x
    l = 1

    while l == 1:
        x = f(x)
        y = f(f(y))
        l = GCD(abs(x - y), n)

    if l == n:
        print('cycle detected')
        # return pollard_ρ(n)

    return l, n // l


if __name__ == '__main__':
    # print(fermat(n))
    print(pollard_ρ(17))
