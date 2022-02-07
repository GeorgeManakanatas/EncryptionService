# -*- coding: utf-8 -*-
'''
decrypting strings and binary inputs
'''
from cryptography.fernet import Fernet

def decrypt_input_simple(encrypted_string, key):
    '''
    Get's string and turns to binary befor encrypting

    Arguments
        encrypted_string(str) : The string to encrypt
        key(str) : the encryption key used

    Returns
        decrypted byte string
    '''
    f = Fernet(bytes(key, encoding='utf-8'))
    decrypted_string = f.decrypt(bytes(encrypted_string, encoding='utf-8'))
    return decrypted_string.decode("utf-8")
