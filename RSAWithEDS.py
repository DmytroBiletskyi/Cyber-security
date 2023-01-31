import rsa
import time


def rsa1():
    file_message = input("Введіть ім'я вхідного файлу: ") + '.txt'
    hash_func = input("Введіть ім'я хеш-функції(‘MD5’, ‘SHA-1’, ‘SHA-224’, ‘SHA-256’, ‘SHA-384’ або ‘SHA-512’): ")
    # генерація ключів (відкритий і закритий)
    (pubkey, privkey) = rsa.newkeys(512)
    # вхідне повідомлення
    with open(file_message, 'r') as f:
        M = f.read().encode("utf8")
    # шифрування повідомлення
    crypto = rsa.encrypt(M, pubkey)
    print(f'Зашифроване повідомлення: {crypto.hex()}')
    # знаходження хешу вхідного повідомлення використовуючи метод хешування SHA-256
    hash = rsa.compute_hash(M, hash_func)
    print(f'Хеш повідомлення: {hash.hex()}')
    # формування підпису
    s = rsa.sign_hash(hash, privkey, hash_func)
    print(f'Підпис: {s.hex()}')
    try:
        # перевірка (верифікація) підпису
        rsa.verify(M, s, pubkey)
        print('ЕЦП вірний')
        # розшифрування закодованого повідомлення
        M = rsa.decrypt(crypto, privkey)
        decrypted_message = input("Введіть ім'я вихідного файлу: ") + '.txt'
        with open(decrypted_message, "w") as f:
            f.write(M.decode("utf-8"))
        print(f'Розшифроване повідомлення: {M.decode("utf8")}')
    except Exception:
        print('ЕЦП не вірний')
    # час завершення виконання програми
    t1 = time.time()
    print("Час виконання програми: ", t1 - t0)
    return M


if __name__ == '__main__':
    # час запуску програми
    t0 = time.time()
    rsa1()
