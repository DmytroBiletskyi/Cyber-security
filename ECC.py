def get_inverse_element(value, max_value):
    # Обрахувати зворотнє значення між 1 - max_value
    for i in range(1, max_value):
        if (i * value) % max_value == 1:
            return i
    return -1


def gcd_x_y(x, y):
    # Обчислити найбільший спільний дільник
    if y == 0:
        return x
    else:
        return gcd_x_y(y, x % y)


def calculate_p_q(x1, y1, x2, y2, a, p):
    # Обрахунок p + q
    flag = 1  # Визначити біт знака
    if x1 == x2 and y1 == y2:
        member = 3 * (x1 ** 2) + a  # Чисельник
        denominator = 2 * y1  # Знаменник
    else:
        member = y2 - y1
        denominator = x2 - x1
        if member * denominator < 0:
            flag = 0
            member = abs(member)
            denominator = abs(denominator)

    # Спростити чисельник і знаменник
    gcd_value = gcd_x_y(member, denominator)
    member = int(member / gcd_value)
    denominator = int(denominator / gcd_value)
    # Знайти зворотній знаменник
    inverse_value = get_inverse_element(denominator, p)
    k = (member * inverse_value)
    if flag == 0:
        k = -k
    k = k % p
    # Обрахувати х3, у3
    x3 = (k ** 2 - x1 - x2) % p
    y3 = (k * (x1 - x3) - y1) % p
    return (x3, y3)


def get_order(x0, y0, a, b, p):
    # Розрахунок порядку еліптичної кривої
    # Розрахунок - р
    x1 = x0
    y1 = (-1 * y0) % p
    temp_x = x0
    temp_y = y0
    n = 1
    while True:
        n += 1
        p_value = calculate_p_q(temp_x, temp_y, x0, y0, a, p)
        if p_value[0] == x1 and p_value[1] == y1:
            print(f'---------- The degree of the elliptic curve is equal to {(n + 1)} ----------')
            return n + 1

        temp_x = p_value[0]
        temp_y = p_value[1]


def calculate_np(G_x, G_y, private_key, a, p):
    # Обрахувати Yb
    temp_x = G_x
    temp_y = G_y
    while private_key != 1:
        p_value = calculate_p_q(temp_x, temp_y, G_x, G_y, a, p)
        temp_x = p_value[0]
        temp_y = p_value[1]
        private_key -= 1
    return p_value


def ecc():
    while True:
        a = int(input('Enter the elliptic curve parameter a: '))
        b = int(input('Enter the elliptic curve parameter b: '))
        p = int(input('Enter the parameter p of the elliptic curve (p is a prime number): '))

        if (4 * (a ** 3) + 27 * (b ** 2)) % p == 0:
            print('The selected elliptic curve cannot be specified for encryption, please select another: ')
        else:
            break
    print('Select point G')
    G_x = int(input("The abscissa of your choice is G_x: "))
    G_y = int(input("The abscissa of your choice is G_y: "))
    # Получити порядок еліптичної кривої
    q = get_order(G_x, G_y, a, b, p)
    # Получити закритий ключ і ключ < порядоку еліптичної кривої q
    kb = int(input(f"Enter the private key kb(<{q}): "))
    # Обрахувати відкритий ключ Yb
    Yb = calculate_np(G_x, G_y, kb, a, p)

    # Початок шифрування
    print('User A calculates:')
    r = int(input(f'Enter the integer r(<{q}): '))
    R = calculate_np(G_x, G_y, r, a, p)  # Оюрахувати R
    P = calculate_np(Yb[0], Yb[1], r, a, p)  # Обрахувати P
    print(f'R - {R}')
    print(f'P - {P}')
    input_file = input("Enter a name for the input file: ") + '.txt'
    with open(input_file, 'r', encoding="utf-8") as f:
        M = f.read()
    cipher_text = []
    for item in M:
        cipher_text.append((ord(item) * P[0]) % p)  # Обрахунок множення тексту і абсциси P
    # Зашифрований текст
    C = [R[0], R[1], cipher_text]
    print(f'Encrypted text: {(C[0], C[1]), C[2]}')
    # Розшифровка
    # Обрахувати private_key * R
    print('User B calculates:')
    Q = calculate_np(C[0], C[1], kb, a, p)
    print(f'Q - {Q}')
    inverse_value = get_inverse_element(Q[0], p)
    m = ''
    for text in C[2]:
        m += chr(text * inverse_value % p)
    output_file = input("Enter a name for the output file: ") + '.txt'
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(m)
    print(f"Deciphered text: {m}")
    return m


if __name__ == '__main__':
    ecc()
