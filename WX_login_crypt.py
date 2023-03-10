import binascii
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from concurrent.futures import ThreadPoolExecutor


def pad(data, block_size):
    padding = block_size - len(data) % block_size
    return data + padding * bytes([padding])


def encrypt_data(decrypted_data, iv, session_key):
    if session_key == "":
        return "Please enter key!"
    if iv == "":
        return "Please enter iv!"
    if decrypted_data == "":
        return "Please enter original data!"

    try:
        base64.decodestring(bytes(session_key, 'utf-8'))
    except binascii.Error:
        return "key no correct base64"
    try:
        base64.decodestring(bytes(iv, 'utf-8'))
    except binascii.Error:
        return "iv no correct base64"

    try:
        aes_iv = base64.b64decode(iv)
        aes_cipher = decrypted_data
        aes_key = base64.b64decode(session_key)

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
        encryptor = cipher.encryptor()
        aes_cipher = pad(aes_cipher.encode(), 16)
        result = encryptor.update(aes_cipher) + encryptor.finalize()

        # print(base64.b64encode(result).decode())
        return str(base64.b64encode(result).decode())
    except Exception as e:
        print(e)
        return str(e)


def decrypt_data(encrypted_data, iv, session_key):
    if session_key == "":
        return "Please enter key!"
    if iv == "":
        return "Please enter iv!"
    if encrypted_data == "":
        return "Please enter encrypt data!"

    try:
        base64.decodestring(bytes(session_key, 'utf-8'))
    except binascii.Error:
        return "key no correct base64"
    try:
        base64.decodestring(bytes(iv, 'utf-8'))
    except binascii.Error:
        return "iv no correct base64"

    try:
        aes_iv = base64.b64decode(iv)
        aes_cipher = base64.b64decode(encrypted_data)
        aes_key = base64.b64decode(session_key)

        cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv), backend=default_backend())
        decryptor = cipher.decryptor()
        result = decryptor.update(aes_cipher) + decryptor.finalize()
        # result = result.decode()
        # result = json.loads(result)

        return str(result[:-int(result[-1])].decode())
    except Exception as e:
        print(e)
        return str(e)


def Batch_GetEn(list):
    result = encrypt_data(list[0], list[1], list[2])
    return result


def Batch_En(datas, iv, key):
    try:
        pool = ThreadPoolExecutor(max_workers=10)
        tmp_list = []
        tmp_data = ""
        for data in datas:
            tmp_list.append([data, iv, key])
        results = pool.map(Batch_GetEn, tmp_list)
        for i in results:
            tmp_data += i
            tmp_data += "\n"
        tmp_data = tmp_data.strip("\n")
        return tmp_data
    except Exception as e:
        print(e)
        return str(e)

# mode = input("??????????????????\n????????????1\n????????????2\n????????????\n????????????")
# if mode == "1":
#     session_key = input("?????????SessionKey: ")
#     iv = input("?????????????????????IV: ")
#     decrypted_data = input("????????????????????????: ")
#
#     result = encrypt_data(decrypted_data, iv, session_key)
#
#     print("????????????????????????: ", result)
#
# elif mode == "2":
#     session_key = input("?????????SessionKey: ")
#     iv = input("?????????????????????IV: ")
#     encrypted_data = input("????????????????????????: ")
#
#     result = decrypt_data(encrypted_data, iv, session_key)
#     print("????????????????????????: ", result)
#
# else:
#     print("error!!!")
