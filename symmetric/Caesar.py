from MSC import MSC

class Caesar(MSC):

    def __init__(self) -> None:
        super().__init__()

    def encrypt(self, cleartext: str):
        return super().encrypt(cleartext, 3)

    def decrypt(self, ciphertext: str):
        return super().decrypt(ciphertext, 3)
