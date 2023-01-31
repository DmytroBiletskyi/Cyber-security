import random
from copy import deepcopy


class PermutationCodes:
    alphabet = 'АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ _,.'

    def __init__(self, message: str):
        self.message = message
        self.key = {}
        self.code = ''
        self.decode = ''
        self.res = []
        self.point = len(self.message)
        self.order_x = {}
        self.order_y = {}
        self.ciphertext_y = ''

    def encrypt_simple_single_permutation(self):
        indexes = random.sample(range(len(self.message)), len(self.message))
        while indexes == sorted(indexes):
            indexes = random.sample(range(len(self.message)), len(self.message))
        for i in indexes:
            self.key[i] = self.message[i]
        for i in self.key:
            self.code += self.key[i]
        return self.code

    def decrypt_simple_single_permutation(self):
        count = 0
        while count != len(self.message):
            self.decode += self.key[count]
            count += 1
        return self.decode

    def encrypt_block_single_permutation(self):
        chunk_size = int(input("Введіть довжину таблиці перестановок: "))
        self.message = chunkify(list(self.message), chunk_size)
        indexes = random.sample(range(len(self.message[0])), len(self.message[0]))
        while indexes == sorted(indexes):
            indexes = random.sample(range(len(self.message[0])), len(self.message[0]))
        for block in self.message:
            for index in indexes:
                self.key[index] = block[index]
                if len(self.key) == len(indexes):
                    self.res.append(self.key)
                    self.key = {}
        for i in self.message:
            for index in indexes:
                self.code += i[index]
        return self.code

    def decrypt_block_single_permutation(self):
        for block in self.res:
            for key in sorted(block):
                self.decode += block[key]
        return self.decode[:self.point]

    def encrypt_vertical_permutation(self):
        passkey = input("Введіть ключ для шифрування: ")
        self.key = {
            int(val): num for num, val in enumerate(passkey)
        }
        while len(self.message) % len(self.key) != 0:
            self.message += ' '
        for index in sorted(self.key.keys()):
            for part in split_len(self.message, len(self.key)):
                self.code += part[self.key[index]]
        return self.code

    def decrypt_vertical_permutation(self):
        count = 0
        lenght = int(len(self.code) / len(self.key))
        while count != lenght:
            for i in self.key:
                self.decode += split_len(self.code, lenght)[i][count]
            count += 1
        return self.decode[:self.point]

    def encrypt_double_permutation(self, xkey, ykey):
        self.order_x = {
            int(val): num for num, val in enumerate(xkey)
        }
        self.order_y = {
            int(val): num for num, val in enumerate(ykey)
        }
        if len(self.order_x) * len(self.order_y) < len(self.message):
            return "Не вірний формат ключів"
        while len(self.message) != len(self.order_x) * len(self.order_y):
            self.message += random.choice(PermutationCodes.alphabet)
        ciphertext_x = ''
        for index in sorted(self.order_x.keys()):
            for part in split_len(self.message, len(self.order_x)):
                ciphertext_x += part[self.order_x[index]]
        for index in sorted(self.order_y.keys()):
            for path in split_len(ciphertext_x, len(self.order_y)):
                self.ciphertext_y += path[self.order_y[index]]
        count = 0
        while count != (len(self.order_x)):
            for block in split_len(self.ciphertext_y, len(self.order_x)):
                self.code += block[count]
            count += 1
        return self.code

    def decrypt_double_permutation(self):
        for y in self.order_y:
            for x in self.order_x:
                self.decode += split_len(self.ciphertext_y, len(self.order_x))[y - 1][x - 1]
        return self.decode[:self.point]

    def grille_cardano(self):
        size = int(input("Введіть розмір решітки: "))
        temp = build_temp(size)
        grill = build_grill(size, temp)
        ch_text = text_to_ch(self.message, grill, size)
        count = 0
        while count != size:
            for block in ch_text:
                self.code += block[count]
            count += 1
        for block in ch_text:
            for symbol in block:
                self.ciphertext_y += symbol
        my_list = split_len(self.ciphertext_y, size)
        # поворот на 0 градусів
        for i in range(size):
            for j in range(size):
                if grill[i][j] == '1':
                    self.decode += my_list[i][j]
        # поворот на 90 градусів
        for i in range(size):
            for j in range(size):
                if grill[size - j - 1][i] == '1':
                    self.decode += my_list[i][j]
        # поворот на 180 градусів
        for i in range(size):
            for j in range(size):
                if grill[size - i - 1][size - j - 1] == '1':
                    self.decode += my_list[i][j]
        # поворот на 270 градусів
        for i in range(size):
            for j in range(size):
                if grill[j][size - i - 1] == '1':
                    self.decode += my_list[i][j]
        print("Результат шифрування: ", self.code)
        print("Результат дешифрування: ", self.decode)


def turn90(mat, size):
    res = [[0] * size for _ in range(size)]
    mat = deepcopy(list(zip(*mat)))
    for i in range(size):
        for j in range(size):
            res[i][j] = mat[i][size - 1 - j]
    return res


def build_temp(size):
    temp = []
    prev = [[0] * (size // 2) for _ in range(size // 2)]
    mats = [prev]
    count = 1
    for i in range(size // 2):
        for j in range(size // 2):
            prev[i][j] = count
            count += 1
    for i in range(3):
        step = turn90(prev, size // 2)
        mats.append(deepcopy(step))
        prev = deepcopy(step)
    for i in range(size // 2):
        temp.append(mats[0][i] + mats[1][i])
    for i in range(size // 2):
        temp.append(mats[3][i] + mats[2][i])
    return temp


def build_grill(size, temp):
    grill = [['0'] * size for _ in range(size)]
    for k in range(1, size ** 2 + 1):
        choice = random.randint(1, 4)
        if choice == 1:
            for i in range(0, size // 2):
                for j in range(0, size // 2):
                    if temp[i][j] == k:
                        grill[i][j] = '1'
        if choice == 2:
            for i in range(0, size // 2):
                for j in range(size // 2, size):
                    if temp[i][j] == k:
                        grill[i][j] = '1'
        if choice == 3:
            for i in range(size // 2, size):
                for j in range(size // 2, size):
                    if temp[i][j] == k:
                        grill[i][j] = '1'
        if choice == 4:
            for i in range(size // 2, size):
                for j in range(0, size // 2):
                    if temp[i][j] == k:
                        grill[i][j] = '1'
    return grill


def text_to_ch(message, grill, size):
    k = 0
    count = 0
    temp = grill
    ch_text = [[''] * size for _ in range(size)]
    while k < size * size:
        for i in range(size):
            for j in range(size):
                if grill[i][j] == '1':
                    ch_text[i][j] = message[k]
                    k += 1
        if k % (size // 2) ** 2 == 0:
            count += 1
            grill = turn90(temp, size)
            temp = deepcopy(grill)
    return ch_text


def chunkify(items, chunk_size):
    matrix = []
    for i in range(0, len(items), chunk_size):
        matrix.append(items[i:i + chunk_size])
    while len(matrix[-1]) != chunk_size:
        matrix[-1].append(random.choice(PermutationCodes.alphabet))
    return matrix


def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]


def main():
    message = input("Введіть повідомлення для шифрування: ").upper()
    choice = input(
        "Виберіть метод для шифрування:\n1-Шифр простої одинарної перестановки\n\
2-Шифр блокової одинарної перестановки\n\
3-Шифр вертикальної перестановки\n\
4-Шифр подвійної перестановки\n\
5-Шифр решітка Кардано\nВаш вибір: ")
    instance = PermutationCodes(message)
    if choice == '1':
        print('Зашифроване повідомлення:', instance.encrypt_simple_single_permutation())
        print('Розшифроване повідомлення:', instance.decrypt_simple_single_permutation())
    elif choice == '2':
        print('Зашифроване повідомлення:', instance.encrypt_block_single_permutation())
        print('Розшифроване повідомлення:', instance.decrypt_block_single_permutation())
    elif choice == '3':
        print('Зашифроване повідомлення:', instance.encrypt_vertical_permutation())
        print('Розшифроване повідомлення:', instance.decrypt_vertical_permutation())
    elif choice == '4':
        print('Зашифроване повідомлення:',
              instance.encrypt_double_permutation((4, 1, 3, 2, 5, 6), (3, 1, 4, 2, 6, 9, 7, 11, 8, 10, 5)))
        print('Розшифроване повідомлення:', instance.decrypt_double_permutation())
    elif choice == '5':
        instance.grille_cardano()
    else:
        print("Невірний вибір!")


if __name__ == '__main__':
    main()
