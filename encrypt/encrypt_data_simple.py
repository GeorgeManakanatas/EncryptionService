# -*- coding: utf-8 -*-
'''
encrypting strings and binary inputs
'''
import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def generate_fernet_key(*args):
    '''
    Generating keys for fernet encryption, either automatically or manually depending on
    the arguments passed to the funcion

    Argments
        *args : The password or empty for automatic generation. No more than one

    Returns
        An auto generated key if no password provided
        A key generated with a hash of the password and the salt used in the hashing
        False if more than one arguments are passed
    '''
    if len(args)==0:

        auto_generated_key = Fernet.generate_key()
        return auto_generated_key
    elif len(args)==1:

        # generate random salt
        salt = base64.urlsafe_b64encode(os.urandom(16)) 
        # for hashing
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        # build a key from the hash of the password in args
        hash_value = kdf.derive(bytes(str(args[0]), 'utf-8'))
        password_generated_key = base64.urlsafe_b64encode(hash_value)
        #
        return password_generated_key, hash_value, salt
    else:
        return False


def encrypt_input_simple(string_or_binary):
    '''
    Get's string or binary and key to encrypt it with. If key not appropriate
    new one is generated and returned instead of the original

    Arguments
        plain_string(str) : The string to encrypt
         

    Returns
        encrypted string
        the generated key used
    '''
    auto_generated_key = generate_fernet_key()
    f = Fernet(auto_generated_key)
    resulting_token = f.encrypt(bytes(string_or_binary, encoding='utf-8'))
    # return the fernet token and the key used
    return resulting_token.decode("utf-8"), auto_generated_key.decode("utf-8")
