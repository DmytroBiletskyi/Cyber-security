import random


class Elgamal:
    def __init__(self):
        self.p = int(input('Input p: '))
        self.a = int(input('Input a: '))
        self.x = int(input('Input x: '))

    def encrypt(self):
        input_file = input("Enter the name of the input file: ")
        with open(input_file, 'r') as f:
            m = int(f.read())
        b = self.a ** self.x % self.p
        y = self.random_select_num(self.p)
        while self.gcd(y, self.p - 1) != 1:
            y = self.random_select_num(self.p)
        self.e = self.a ** y % self.p
        self.k = (b ** y * m) % self.p
        return (self.e, self.k)

    def decrypt(self):
        output_file = input("Enter the name of the output file: ")
        m = self.k * self.e ** (self.p - 1 - self.x) % self.p
        result = [str((self.e, self.k)), str(m)]
        with open(output_file, "w") as f:
            f.writelines("%s\n" % i for i in result)
        return m

    def gcd(self, x, y):
        if y == 0:
            return x
        else:
            return self.gcd(y, x % y)

    def random_select_num(self, p):
        rand_num = random.randint(2, p - 2)
        return rand_num


elgamal = Elgamal()
print(f'Encrypted message: {elgamal.encrypt()}')
print(f'Decrypted message: {elgamal.decrypt()}')
