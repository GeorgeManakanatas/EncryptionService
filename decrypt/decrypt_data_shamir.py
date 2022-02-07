# -*- coding: utf-8 -*-
'''
decrypting data with shamir secret sharing
'''
import base64
import shamir
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from decrypt.decrypt_data_simple import decrypt_input_simple

def decrypt_input_shamir(string_or_binary, the_shares, the_salt):
    # try to get the secret
    the_secret = shamir.recover_secret(the_shares)
    # get the hash from the secret and the salt
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=the_salt.encode('utf-8'),
        iterations=100000,
        backend=default_backend()
    )
    hash_value = kdf.derive(bytes(str(the_secret), 'utf-8'))
    generated_key = base64.urlsafe_b64encode(hash_value)
    # decrypt information
    the_information = decrypt_input_simple(string_or_binary, generated_key.decode('utf-8'))
    #
    return the_information