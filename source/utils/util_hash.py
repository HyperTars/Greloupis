import hashlib


def hash_encode(data: str):
    return hashlib.sha512(data.encode('utf-8')).hexdigest()
