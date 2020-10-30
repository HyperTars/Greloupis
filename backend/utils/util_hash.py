import hashlib
import random


def util_hash_encode(data: str):
    return util_hash_sha512(data)


def util_hash_sha512(data: str):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()


def util_hash_md5_with_salt(data: str, salt: str):
    md5_str = hashlib.md5()
    md5_str.update((data + salt).encode('utf-8'))
    return md5_str.hexdigest()


def util_hash_create_salt(length=4):
    salt = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    len_chars = len(chars) - 1
    ran = random.Random()
    for i in range(length):
        salt += chars[ran.randint(0, len_chars)]
    return salt
