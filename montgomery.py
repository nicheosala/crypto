from accessories import *


def reduction(x: int) -> int:

    assert 1 < x <= R * N

    return x * R % N


def dec_to_bin(num: int) -> str:
    return f'{int(str(num), 10):0>5b}'


def multiplication(red_A: int, red_B: int) -> int:
    '''
    Receive the reduced values of A and B and compute their
    Montgomery product.
    '''
    x = dec_to_bin(0)
    red_A = dec_to_bin(red_A)
    red_B = dec_to_bin(red_B)

    print(f'A:\t\t{red_A}')
    print(f'B:\t\t{red_B}')

    for i in range(len(red_A)):

        print(f'x:\t\t{x}')

        if red_A[- 1 - i] == '0':
            A_B = dec_to_bin(0)
        else:
            A_B = red_B
        print(f'A[{i}] * B:\t{A_B}')
        print('-'*30)

        x = dec_to_bin(int(x, b) + int(A_B, b))
        print(f'x:\t\t{x}')

        t = dec_to_bin(((int(x[-1]) * N * N0) % N))
        print(f't:\t\t{t}')
        print('-'*30)

        x = dec_to_bin((int(x, b) + int(t, b)) // b)

    print(f'x:\t\t{x}')

    return int(x, b)


if __name__ == '__main__':
    b: int = 2
    d: int = 0

    N: int = 21

    R: int = 1
    while R < N:
        d += 1
        R *= b

    assert R > N
    assert coprime(N, R)

    _, N_INV, R_INV = EEA(N, R)
    N_INV = - N_INV

    R_SQ: int = pow(R, 2, N)

    N0: int = (- inverse(N & 1, b)) % b

    print(f'R: {R}, N: {N}, N_INV: {N_INV}, R_INV: {R_INV}, N0: {N0}')

    multiplication(reduction(3), reduction(17))
