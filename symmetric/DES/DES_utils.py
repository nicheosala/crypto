def bin_to_hex(bin: str) -> str:
    return f'{int(bin, 2):0>8X}'


def hex_to_bin(hex: str) -> str:
    return f'{int(hex, 16):0>64b}'


def bin_to_dec(binary: int) -> int:
    return int(str(binary), 2)


def dec_to_bin(num: int) -> str:
    return f'{int(str(num), 10):0>4b}'


def permute(data, arr, n):
    return ''.join(data[arr[i] - 1] for i in range(n))


def xor(a, b):
    assert(len(a) == len(b))
    return ''.join('0' if a[i] == b[i] else '1' for i in range(len(a)))

# TODO review
# shifting the bits towards left by nth shifts
def shift_left(k, nth_shifts):
    s = ""
    for i in range(nth_shifts):
        for j in range(1,len(k)):
            s = s + k[j]
        s = s + k[0]
        k = s
        s = "" 
    return k  