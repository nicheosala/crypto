'''
Nicolò Sala, 30 giugno 2021
Ho provato a replicare l'esperimento descritto nelle slide riguardanti la crittanalisi differenziale
(slide 13 e seguenti) e ci sono riuscito!
'''

from operator import xor
from functools import reduce


def bitwise_and(bit_0: str, bit_1: str) -> int:
    return int(bit_0, 2) & int(bit_1, 2)

def bitwise_xor(bit_0: str, bit_1: str) -> int:
    return int(bit_0, 2) ^ int(bit_1, 2)


def N_bits(string, N):
    '''
    Takes a binary string and converts it to a binary string of EXACTLY N bits.
    '''
    return f'{int(string, 2):0>{N}b}'


def and_then_xor(i: str, j: str):
    '''
    Take two bit strings. & bits in same position, then reduce all xor-ing.
    '''
    return reduce(xor, map(bitwise_and, i, j))


def binary_numbers(N):
    '''
    Restituisce una tupla contenente stringhe binarie ordinate di tutti i
    numeri da 0 a 2 ** N codificati con N bits.
    '''
    return (N_bits(bin(i), N) for i in range(2 ** N))


def solve_linear(A, X, B, Y):
    '''
    Risolve un'equazione lineare binaria del tipo:
    a1 & x1 ^ a2 & x2 ^ ... = b1 & y1 ^ b2 & y2 ^ ...
    '''
    return and_then_xor(A, X) == and_then_xor(B, Y)


def linear(S, N):
    '''
    Questa funzione riceve come parametri:
    - S: la S_box che vogliamo analizzare. Essa è una black-box
    - bits: è il numero di bits in input, assunto uguale al numero di bits in output alla S_box
    '''
    results = []
    for A in binary_numbers(N):
        line = []
        for B in binary_numbers(N):
            ctr = sum(solve_linear(A, X, B, S(X)) for X in binary_numbers(N))
            line.append(ctr - S_BOX_SIZE // 2)
        results.append(line)
    for line in results:
        print(line)


def differential(S, N):
    results = []
    for dX in binary_numbers(N):
        line = []
        for dY in binary_numbers(N):
            ctr = sum(solve_differential(I, dX, dY, S) for I in binary_numbers(N))
            line.append(ctr)
        results.append(line)
    for line in results:
        print(line)


def solve_differential(I, dX, dY, S):
    return str_xor(S(I), S(str_xor(I, dX))) == dY

def str_xor(s1: str, s2: str) -> str:
    return N_bits(bin(bitwise_xor(s1, s2)), len(s1))


S_box_hex = {
    '0': 'E',
    '1': '4',
    '2': 'D',
    '3': '1',
    '4': '2',
    '5': 'F',
    '6': 'B',
    '7': '8',
    '8': '3',
    '9': 'A',
    'A': '6',
    'B': 'C',
    'C': '5',
    'D': '9',
    'E': '0',
    'F': '7'
}


def hex_to_bin(item): return (
    f'{int(item[0], 16):0>{4}b}', f'{int(item[1], 16):0>{4}b}')


S_box = dict(map(hex_to_bin, S_box_hex.items()))
# print(S_box)

S_BOX_SIZE = len(S_box)


def S(x): return S_box[x]


def trivial_cipher():
    linear(S, 4)


def add_round_key(k, x):
    return list(map(xor, x, k))


def perm():
    pass


def simple_cipher():
    '''
    TODO
    '''
    x = []
    key = []
    for i in range(3):
        x = add_round_key(x, key[i:16*(i + 1)])
        x = S(x[:4]) + S(x[4:8]) + S(x[8:12]) + S(x[12:])
        perm()
    add_round_key(key[48:64])
    S(x)
    add_round_key(key[64:80])


if __name__ == '__main__':
    linear(S, 4)
    differential(S, 4)
