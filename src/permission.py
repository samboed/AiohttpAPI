import bcrypt


def hash_password(raw_password: bytes) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(raw_password, salt)
