from random import randint


def shamir():
    message = input("Enter the name of the input file: ") + '.txt'
    p = int(input('Input p: '))
    qa = int(input('Input qa: '))
    qb = int(input('Input qb: '))
    ka = select_keys(qa, p)
    print(f'ka - {ka}')
    kb = select_keys(qb, p)
    print(f'kb - {kb}')
    with open(message, 'r') as msg:
        m = int(msg.read())
    ya = m**ka % p
    yb = ya**kb % p
    c = yb**qa % p
    print(f'Encrypted message: {c}')
    m = c**qb % p
    print(f'Decrypted message: {m}')
    lst = [c, m]
    result_file = input("Enter the name of the output file: ") + '.txt'
    with open(result_file, "w") as f:
        f.writelines("%s\n" % item for item in lst)
    return c, m


def select_keys(b, p):
    key = random_num(p)
    while key * b % (p - 1) != 1:
        key = random_num(p)
    return key


def random_num(p):
    rand_num = randint(2, p-2)
    return rand_num


if __name__ == '__main__':
    shamir()
