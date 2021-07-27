'''
Nicolò, 10 luglio 2021

Tentativo di riunire tutti i cifrari a sostituizione in un unico file.
Non posso dedicarci altro tempo, causa poco tempo pre esame :(
'''


from symmetric.all import vigenere, vigenere_decrypt, vigenere_encrypt


class PSC:
    '''
    Polyalphabetic substitution cipher.
    '''

    def __init__(self, *maps: tuple[tuple]) -> None:
        assert len(maps) >= 1
        self.maps = maps
        self.L = len(maps)

    def encrypt(self, plaintext: str) -> str:
        ciphertext = []
        for i in range(len(plaintext)):
            encrypt_char = self.maps[i % self.L][0]
            ciphertext += encrypt_char(plaintext[i])
        return ''.join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        cleartext = []
        for i in range(len(ciphertext)):
            decrypt_char = self.maps[i % self.L][1]
            cleartext += decrypt_char(ciphertext[i])
        return ''.join(cleartext)


class MSC(PSC):
    '''
    Monoalphabetic substitution cipher.
    '''

    def __init__(self, encryption, decryption) -> None:
        super().__init__((encryption, decryption))


class ShiftCipher:
    '''
    Caesar's and Vigenere's are examples of shift ciphers.
    '''

    def __init__(self) -> None:
        pass

    def __shift(self, text, key):
        return ''.join(map(lambda char: chr(ord(char) + key), text))

    def encrypt(self, cleartext: str, encryption_key):
        return self.__shift(cleartext, encryption_key)

    def decrypt(self, ciphertext: str, decryption_key):
        return self.__shift(ciphertext, -decryption_key)


class Caesar(MSC):
    '''
    Caesar's cipher.
    '''

    def __init__(self) -> None:
        super().__init__(self.__encrypt, self.__decrypt)

    def __encrypt(self, cleartext: str):
        return ShiftCipher().encrypt(cleartext, 3)

    def __decrypt(self, ciphertext: str):
        return ShiftCipher().decrypt(ciphertext, 3)


class Vigenere():

    def __init__(self, L: int) -> None:
        maps = []
        for i in range(L):
            enc = vigenere_encrypt(key = L)
            dec = vigenere_decrypt(key = L)
        # TODO

    def __vigenere(text, key, alphabet, encryption=1):
        def key_shift(i): return alphabet.index(key[i % len(key)]) * encryption
        return ShiftCipher().__shift(text, key_shift, alphabet)


    def vigenere_encrypt(self, cleartext, key, alphabet):
        return self.__vigenere(cleartext, key, alphabet)


    def vigenere_decrypt(self, ciphertext, key, alphabet):
        return self.__vigenere(ciphertext, key, alphabet, -1)


if __name__ == '__main__':
    text = 'ciao mamma'

    print('\nCesare')
    caesar = Caesar()
    c = caesar.encrypt(text)
    p = caesar.decrypt(c)
    print(f'ciphertext:\t{c}')
    print(f'plaintext:\t{p}')

    print('Vigenere')
    v = Vigenere()
