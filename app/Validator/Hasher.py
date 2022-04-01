import binascii
import hashlib
import os
import uuid
import base64

"""
class for generating hashes and tokens
"""


class Hasher:

    def __init__(self):
        ...

    @staticmethod
    def hash(password, salt=None):
        """
        :param password: password to hash
        :param salt: salt to be added to password. Randomly generated if not specified
        :return: hashed password
        """
        salt = salt or hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pw_hash = hashlib.pbkdf2_hmac('sha512',
                                      password.encode('utf-8'),
                                      salt,
                                      100000)
        pw_hash = binascii.hexlify(pw_hash)
        return (salt + pw_hash).decode('ascii')

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        :param stored_password: password stored in DB
        :param provided_password: password submitted by user
        :return: True if un-hashed password is equal to the provided password
        """
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pw_hash = hashlib.pbkdf2_hmac('sha512',
                                      provided_password.encode('utf-8'),
                                      salt.encode('ascii'),
                                      100000)
        pw_hash = binascii.hexlify(pw_hash).decode('ascii')
        return pw_hash == stored_password

    @staticmethod
    def generate_token():
        """
        :return: a random UUID converted to hex
        """
        return uuid.uuid4().hex

    @staticmethod
    def cal_request_sig(user_agent, client_ip, cookies):
        """
        create a request signature by hashing each of the params, converting them to string, joining them and
        encoding them
        :param user_agent:
        :param client_ip:
        :param cookies:
        :return: encoded request signature
        """
        rs_bytes = "".join([str(hash(user_agent)), str(hash(client_ip)), str(hash(cookies))]).encode('ascii')
        rs_bytes = base64.b64encode(rs_bytes)
        return rs_bytes.decode('ascii')
