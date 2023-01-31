from random import randint


def rabin():
    p = select_keys()
    print(f'p = {p}')
    q = select_keys()
    print(f'q = {q}')
    n = p * q
    input_file = input("Enter the name of the input file: ") + '.txt'
    with open(input_file, 'r') as f:
        m = int(f.read())
    c = m**2 % n
    print(f'Encrypted message: {c}')
    k = int((p + 1) / 4)
    l = int((q + 1) / 4)
    print(f'k = {k}')
    print(f'l = {l}')
    x = c**k % p
    y = c**l % q
    print(f'x = {x}')
    print(f'y = {y}')
    m1 = x % p
    m11 = y % q
    m2 = x % p
    m22 = -y % q
    m3 = -x % p
    m33 = y % q
    m4 = -x % p
    m44 = -y % q
    print(f'(m1, m11) = {(m1, m11)}')
    print(f'(m2, m22) = {(m2, m22)}')
    print(f'(m3, m33) = {(m3, m33)}')
    print(f'(m4, m44) = {(m4, m44)}')
    result = [(m1, m11), (m2, m22), (m3, m33), (m4, m44)]
    for m in result:
        if m[0] == m[1]:
            print(f'Decrypted message: {m}: {m[0]}')
            output_file = input("Enter the name of the output file: ") + '.txt'
            res = [c, m[0]]
            with open(output_file, "w") as f:
                f.writelines("%s\n" % i for i in res)
            return m
    return m


def select_keys():
    key = random_num()
    while key % 4 != 3:
        key = random_num()
    return key if is_prime(key) else select_keys()


def random_num():
    rand_num = randint(100, 500)
    return rand_num


def is_prime(a):
    if a % 2 == 0:
        return a == 2
    d = 3
    while d * d <= a and a % d != 0:
        d += 2
    return d * d > a


if __name__ == '__main__':
        rabin()
