"""
Nicolò Sala, 25th June 2021
General implementation for shift ciphers like:
- Caesar's cipher
- Monoalphabetic substitution ciphers
- Vigenere's cipher

Maybe I'll be able to generalize this to polyalphabetic substitution ciphers.

Can I maintain this generality but reduce code complexity?
In other words: is there a better method to find out the key_shift parameter?
"""


def shift_letter(letter, key_shift, alphabet):
    return letter if letter not in alphabet else alphabet[(alphabet.index(letter) + key_shift) % len(alphabet)]


def shift(text, key_shift, alphabet):
    return ''.join(shift_letter(letter, key_shift(i), alphabet) for (i, letter) in enumerate(text))


def vigenere(text, key, alphabet, encryption=1):
    '''
    'encryption' == 1 for encryption, == -1 for decryption
    '''
    def key_shift(i): return alphabet.index(key[i % len(key)]) * encryption
    return shift(text, key_shift, alphabet)


def vigenere_encrypt(cleartext, key, alphabet):
    return vigenere(cleartext, key, alphabet)


def vigenere_decrypt(ciphertext, key, alphabet):
    return vigenere(ciphertext, key, alphabet, -1)


def msc(text, key, alphabet, encryption=1):
    def key_shift(_): return key * encryption
    return shift(text, key_shift, alphabet)


def msc_encrypt(cleartext, key, alphabet):
    return msc(cleartext, key, alphabet)


def msc_decrypt(ciphertext, key, alphabet):
    return msc(ciphertext, key, alphabet, -1)


def caesar_encrypt(cleartext, alphabet):
    return msc_encrypt(cleartext, 3, alphabet)


def caesar_decrypt(ciphertext, alphabet):
    return msc_decrypt(ciphertext, 3, alphabet)


if __name__ == '__main__':

    print("\n**Vigenere**\n")

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    text = 'The quick brown fox jumps over 13 lazy dogs.'
    key = 'crypto'

    # All the letters of the key must be inside the alphabet.
    assert(all(letter in alphabet for letter in key))

    ciphertext = vigenere_encrypt(text, key, alphabet)
    cleartext = vigenere_decrypt(ciphertext, key, alphabet)

    print(f"Text: {text}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Cleartext: {cleartext}")

    print("\n**Caesar**\n")

    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    text = 'The quick brown fox jumps over 13 lazy dogs.'
    key = 'crypto'

    ciphertext = caesar_encrypt(text, alphabet)
    cleartext = caesar_decrypt(ciphertext, alphabet)

    print(f"Text: {text}")
    print(f"Ciphertext: {ciphertext}")
    print(f"Cleartext: {cleartext}")
