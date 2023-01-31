from random import randint
import hashlib

def dsa():
    m = input('Введіть m: ').encode()
    p = int(input('Введіть p: '))
    q = int(input('Введіть q: '))
    x = int(input('Введіть x: '))
    k = int(input('Введіть k: '))
    h = random_num(p)
    g = int(h ** ((p - 1) / q) % p)
    while h**((p-1)/q) % p < 1 or g < 1:
        h = random_num(p)
        g = int(h ** ((p - 1) / q) % p)
    print(f'h - {h}')
    print(f'g - {g}')
    y = g**x % p
    print(f'y - {y}')
    # підпис повідомлення
    choice = int(input('Виберіть алгоритм хешування: 1 - MD-5, 2 - SHA-1: '))
    r = (g**k % p) % q
    if choice == 1:
        s = (k**(q-2) * (choice_hash(m, choice) + x * r)) % q
        # перевірка підпису
        w = s ** (q - 2) % q
        u1 = (choice_hash(m, choice) * w) % q
        print(f'Підпис: r - {r}, s - {s}')
        u2 = (r * w) % q
        v = ((g**u1 * y**u2) % p) % q
        print(f'v - {v}')
        if v == r:
            print('Підпис вірний')
        else:
            print('Підпис не вірний')
    elif choice == 2:
        s = (k ** (q - 2) * (choice_hash(m, choice) + x * r)) % q
        # перевірка підпису
        w = s ** (q - 2) % q
        u1 = (choice_hash(m, choice) * w) % q
        print(f'Підпис: r - {r}, s - {s}')
        u2 = (r * w) % q
        v = ((g ** u1 * y ** u2) % p) % q
        if v == r:
            print('Підпис вірний')
        else:
            print('Підпис не вірний')
    return m


def choice_hash(m, n):
    if n == 1:
        h_m = int.from_bytes(hashlib.md5(m).digest(), 'big')
        return h_m
    elif n == 2:
        h_m = int.from_bytes(hashlib.sha1(m).digest(), 'big')
        return h_m


def random_num(p):
    rand_num = randint(2, p-2)
    return rand_num


if __name__ == '__main__':
    dsa()
