import binascii
import hashlib
import os


class Hasher:

    @staticmethod
    def hash(password, salt=None):
        salt = salt or hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pw_hash = hashlib.pbkdf2_hmac('sha512',
                                      password.encode('utf-8'),
                                      salt,
                                      100000)
        pw_hash = binascii.hexlify(pw_hash)
        return (salt + pw_hash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pw_hash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pw_hash = binascii.hexlify(pw_hash).decode('ascii')
        return pw_hash == stored_password
