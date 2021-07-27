from Cryptoscheme import Cryptoscheme


class MSC(Cryptoscheme):

    def __init__(self) -> None:
        super().__init__()

    def _shift(self, text, key):
        return ''.join(map(lambda char: chr(ord(char) + key), text))

    def encrypt(self, cleartext: str, encryption_key):
        return self._shift(cleartext, encryption_key)

    def decrypt(self, ciphertext: str, decryption_key):
        return self._shift(ciphertext, -decryption_key)
