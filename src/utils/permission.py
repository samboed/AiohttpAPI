import bcrypt

ENCODING = 'utf-8'


def encode_password(password: str) -> bytes:
    return password.encode(ENCODING)


def decode_password(password: bytes) -> str:
    return password.decode(ENCODING)


def hash_password(password: str) -> str:
    password_bytes = encode_password(password)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return decode_password(hashed_password)


def check_password(password: str, reference_password) -> bool:
    hashed_password = encode_password(password)
    hashed_reference_password = encode_password(reference_password)
    return bcrypt.checkpw(hashed_password, hashed_reference_password)
