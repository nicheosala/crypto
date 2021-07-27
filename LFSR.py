from functools import reduce
from operator import xor, and_
from typing import Iterator


def LFSR(C: tuple[int], S: list[int]):
    '''
    Linear Feedback Shift Register

    Based on "Block cipher AES; Stream Ciphers, slide 27 and ss.,
    with some optimizations.

    The convention w.r.t. the slides is changed, so that there's no confusion btw indices of C and S.
    Both C and S starts from index 0: I don't know how to explain it better.
    '''

    assert len(S) == len(C) and len(S) > 0
    def binary(L): return all(l in [0, 1] for l in L)
    assert binary(S)
    assert binary(C)

    while True:
        S.insert(0, reduce(xor, map(and_, C, S)))
        yield S.pop()


def encrypt(cleartext: list[int], stream_bits: list[int]) -> Iterator[int]:
    return map(xor, cleartext, stream_bits)


def decrypt(ciphertext: list[int], stream_bits: list[int]) -> Iterator[int]:
    return map(xor, ciphertext, stream_bits)


if __name__ == '__main__':

    C = (0, 1, 0, 0, 1)  # c1, c2, c3... c0 is assumed always equal to 1.
    S = [1, 1, 0, 1, 1]

    lfsr = LFSR(C, S)

    for _ in range(10):
        print(next(lfsr))
