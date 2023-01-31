from main import np
from main import LA


def Hyll_Cipher():
    text_numbers = []
    key_code = []
    res = []
    encrypted_message = ''
    key = 'АКЛІМАТИЗУВАТИСЯ'
    alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ _,.'
    message = input('Введіть своє повідомлення для шифрування: ').upper()
    if not message:
        message = 'Я, БІЛЕЦЬКИЙ ДМИТРО ОЛЕКСАНДРОВИЧ, СТУДЕНТ УНІВЕРСИТЕТУ'
    for symbol in message:
        if symbol in alphabet:
            text_numbers.append(alphabet.find(symbol))
        else:
            print('Не допустимий символ!')
            return 0
    for symbol in key:
        if symbol in alphabet:
            key_code.append(alphabet.find(symbol))
    key_matrix = np.array(chunkify(key_code, 4))
    text_matrix = chunkify(text_numbers, 4)
    for text_block in text_matrix:
        res.append((np.array(text_block).dot(key_matrix)) % 37)
    for block in res:
        for number in block:
            encrypted_message += alphabet[number]
    print('Зашифроване повідомлення:', encrypted_message)
    # decryption()
    text_numbers.clear()
    for symbol in encrypted_message:
        if symbol in alphabet:
            text_numbers.append(alphabet.find(symbol))
    text_matrix = chunkify(text_numbers, 4)
    # Знаходимо детермінант матриці ключа
    det_matrix_key = int(LA.det(key_matrix))
    # Розширений алгоритм Евкліда
    determinant = gcdex(det_matrix_key, len(alphabet))
    # Обрахунок оберненого детермінанту елементу
    key_matrix_inverse_determinant = inverse_determinant_element(det_matrix_key, determinant[1])
    result_0 = []
    alliance_matrix = np.array(chunkify(algebraic_additions(key_matrix), 4))
    for i in alliance_matrix:
        for j in i:
            if j < 0:
                j = abs(j) % 37
                result_0.append(-j)
            else:
                j = j % 37
                result_0.append(j)
    result_0 = np.array(chunkify(result_0, 4))
    result = []
    for i in result_0:
        for j in i:
            if j < 0:
                j = (abs(j) * key_matrix_inverse_determinant) % 37
                result.append(-j)
            else:
                j = (j * key_matrix_inverse_determinant) % 37
                result.append(j)
    result = np.array(chunkify(result, 4))
    result_transpose = result.transpose()
    inverse_modulo_to_the_key_matrix = []
    for i in result_transpose:
        for j in i:
            if j < 0:
                j = 37 + j
                inverse_modulo_to_the_key_matrix.append(j)
            else:
                inverse_modulo_to_the_key_matrix.append(j)
    inverse_modulo_to_the_key_matrix = np.array(chunkify(inverse_modulo_to_the_key_matrix, 4))
    message_decryption = []
    for i in text_matrix:
        message_decryption.append((np.array(i).dot(inverse_modulo_to_the_key_matrix)) % 37)
    message_decryption = [x for l in message_decryption for x in l]
    decrypted_message = ''
    for number in message_decryption:
        decrypted_message += alphabet[number]
    print('Дешифроване повідомлення:', decrypted_message)


# Функція для розбиття списку на блоки
def chunkify(items, chunk_size):
    matrix = []
    for i in range(0, len(items), chunk_size):
        matrix.append(items[i:i + chunk_size])
    while len(matrix[-1]) != 4:
        matrix[-1].append(33)
    return matrix


# Розширений алгоритм Евкліда
def gcdex(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, x, y = gcdex(b, a % b)
        return d, y, x - y * (a // b)


# Обернений детермінанту елемент
def inverse_determinant_element(det, x):
    if det < 0 and x > 0:
        return x
    elif det > 0 and x < 0:
        return 37 + x
    elif det > 0 and x > 0:
        return x
    elif det < 0 and x < 0:
        return -x


# Алгебраїчні доповнення
def algebraic_additions(key_matrix):
    result = []
    for i in range(len(key_matrix)):
        for j in range(len(key_matrix[i])):
            Mi = np.delete(key_matrix, [i], axis=0)
            Mij = np.delete(Mi, [j], 1)
            if i + j == 0:
                result.append((int_r(LA.det(Mij))))
            elif (i + j) % 2 == 0:
                result.append((int_r(LA.det(Mij))))
            else:
                result.append(-(int_r(LA.det(Mij))))
    return result


def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num


def main():
    Hyll_Cipher()


if __name__ == '__main__':
    main()
