# -*- coding: utf-8 -*-
'''
encrypting strings and binary inputs with shamir secret sharing
'''
import json
import base64
import os
import shamir
from cryptography.fernet import Fernet
from encrypt.encrypt_data_simple import generate_fernet_key

def encrypt_input_shamir(string_or_binary, keys_all, keys_min):
    '''
    Get's string or binary and key to encrypt it with. If key not appropriate
    new one is generated and returned instead of the original

    Arguments
        string_or_binary(str) : The string to encrypt
        keys_all(int) : The number of keys generated
        keys_min(int) : The min number of keys that should decrypt the message

    Returns
        A json containing the encrypted data, the shares, the secret and the minimum shares needed to recover the secret
    '''
    the_secret, the_shares = shamir.make_random_shares(keys_min, keys_all) # get secret and shares
    # print('\n\n the recovered secret from the shares is : ', shamir.recover_secret(the_shares))
    password_generated_key, hash_value, salt = generate_fernet_key(the_secret)
    # use the key to encrypt the information
    f = Fernet(password_generated_key)
    resulting_token = f.encrypt(bytes(string_or_binary, encoding='utf-8'))
    # return the fernet token and the key used
    return_json = {}
    return_json['minimum'] = keys_min
    return_json['secret'] = the_secret
    return_json['shares'] = the_shares
    # return_json['hash'] = hash_value
    return_json['salt'] = salt.decode('utf-8')
    return_json['token'] = resulting_token.decode('utf-8')
    return json.dumps(return_json)
