class RSA:
    def __init__(self, message, p, q, e):
        self.n = p * q
        self.message = message
        self.p = p
        self.q = q
        self.e = e

    def encrypt(self):
        encrypted_message = self.message**self.e % self.n

        return encrypted_message

    def decrypt(self):
        Fi = (self.p - 1) * (self.q - 1)
        gcd, x, y = self.gcd_extended(Fi, self.e)
        if y < 0:
            d = y % Fi
        else:
            d = y
        decrypted_message = self.encrypt()**d % self.n

        return decrypted_message

    def gcd_extended(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.gcd_extended(b % a, a)
            return gcd, y - (b // a) * x, x


rsa = RSA(12, 13, 17, 133)
print(f'Encrypted message: {rsa.encrypt()}')
print(f'Decrypted message: {rsa.decrypt()}')
