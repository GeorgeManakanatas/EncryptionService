# -*- coding: utf-8 -*-
'''
Routing of incoming requests
'''
import ast
import json
from flask import Flask, request, jsonify, Response
from tests import tests
from encrypt.encrypt_data_simple import encrypt_input_simple
from encrypt.encrypt_data_shamir import encrypt_input_shamir
from decrypt.decrypt_data_simple import decrypt_input_simple
from decrypt.decrypt_data_shamir import decrypt_input_shamir
from system_checks.memory_checks import check_memory_requirement

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():
    '''
    Sanity check route to see if the server is running
    '''
    # returning 200 code if serivce is runing
    return jsonify(success=True, message='Hello world!'), 200


@app.route('/tests', methods=['GET'])
def unit_tests():
    '''
    Runs the unit tests and returns the result
    '''
    response_mesage = str(tests.main())
    return Response(response_mesage, status=200, mimetype='text/csv')


@app.route('/check', methods=['GET'])
def check_status():
    '''
    Sanity check route to see if the server is running
    '''
    return Response("{'Service status':'Running'}", status=200,
                    mimetype='application/json')


@app.route('/encrypt-data/simple', methods=['POST', 'GET'])  
def encrypt_data_simple():
    '''
    Encrypt string or binary that is passed in the request form
    '''
    if request.method == 'GET':
        return jsonify(success=True), 200
    elif request.method == 'POST':
        data = request.form.get('data')  # the actual string / binary
        if data is None:
            return Response('{"error":"Encryption data must be provided"}',
                            status=422,
                            mimetype='application/json')

        token, key = encrypt_input_simple(data)
        print(' token ', token, ' key ', key)
        resp = {}
        resp['token'] = token
        resp['key'] = key
        return Response(json.dumps(resp),
                        status=200,
                        mimetype='application/json')
    else:
        print('This should not be here')
        return Response('Internal server error',
                        status=500,
                        mimetype='application/json')


@app.route('/encrypt-data/shamir', methods=['POST', 'GET'])  
def encrypt_data():
    '''
    Encrypt string or binary that is passed in the request form with shamir secret sharing
    '''
    if request.method == 'GET':
        return jsonify(success=True), 200
    elif request.method == 'POST':
        keys_all = request.args.get('keys_all') # the number of keys to generate
        keys_min = request.args.get('keys_min') # the min number needed to decrypt
        data = request.form.get('data')  # the actual string / binary
        if data is None:
            return Response('{"error":"Encryption data must be provided"}',
                            status=422,
                            mimetype='application/json')

        return_value = encrypt_input_shamir(data, int(keys_all), int(keys_min))
        return Response(return_value,
                        status=200,
                        mimetype='application/json')
    else:
        print('This should not be here')
        return Response('Internal server error',
                        status=500,
                        mimetype='application/json')

@app.route('/encrypt-file', methods=['GET', 'POST'])
def encrypt_file():
    '''
    Encrypt the file the path to wich is passed in the request form
    '''
    if request.method == 'GET':
        return Response('{"success":True}', status=200,
                        mimetype='application/json')
    if request.method == 'POST':
        file_path = request.form.get('filepath')
        file_name = request.form.get('filename')
        if (file_path is None) or (file_name is None):
            return Response('{"error":"Filename and path must be provided"}',
                            status=422,
                            mimetype='application/json')
        if ('shared_folder' not in file_path):
            return Response('{"error":"File must be in shared folder directory"}',
                            status=422,
                            mimetype='application/json')
        # check if enough memory to read the file
        check_memory_requirement(file_path+file_name)
        # if there is no abort read the file
        target_file = open(file_path+file_name, "r")
        file_data = target_file.read()
        target_file.close()
        # encrypt contents
        token, key = encrypt_input_simple(str(file_data))
        # save to drive
        enc_file = open(file_path+'encFile.txt', "w")
        enc_file.write(token)
        enc_file.close()
        # return reply
        resp = {}
        resp['encrypted_file'] = file_path+'encFile.txt'
        resp['key'] = key
        return Response(json.dumps(resp),
                        status=200,
                        mimetype='application/json')


@app.route('/decrypt-data/simple', methods=['GET', 'POST'])
def dencrypt_data_simple():
    '''
    Dencrypt string or binary that is passed in the request form with shamir secret sharing
    '''
    if request.method == 'GET':
        return jsonify(success=True), 200
    if request.method == 'POST':
        data = request.form.get('data')  # the actual string / binary
        key = request.form.get('key')  # the key used to encrypt it
        if (data is None) or (key is None):
            return Response('{"error":"Data and key must be provided"}',
                            status=422,
                            mimetype='application/json')

        decrypted_data = decrypt_input_simple(data, key)
        resp = {}
        resp['decrypted'] = str(decrypted_data)
        return Response(json.dumps(resp),
                        status=200,
                        mimetype='application/json')

@app.route('/decrypt-data/shamir', methods=['POST', 'GET'])
def dencrypt_data_shamir():
    '''
    Dencrypt string or binary that is passed in the request form
    '''
    if request.method == 'GET':
        return jsonify(success=True), 200
    if request.method == 'POST':
        the_data = request.form.get('data') # the actual string / binary
        the_shares = request.form.get('shares') # the shares from shamir
        the_salt = request.form.get('salt') # the salt for the secret
        if (the_data is None) or (the_shares is None) or (the_salt is None):
            return Response('{"error":"Data salt and shares must be provided"}',
                            status=422,
                            mimetype='application/json')
        # turn the shares back to array
        the_shares = ast.literal_eval(the_shares)
        decrypted_data = decrypt_input_shamir(the_data, the_shares, the_salt)
        resp = {}
        resp['decrypted'] = str(decrypted_data)
        return Response(json.dumps(resp),
                        status=200,
                        mimetype='application/json')


@app.route('/decrypt-file', methods=['GET', 'POST'])
def dencrypt_file():
    '''
    Dencrypt file
    '''
    if request.method == 'GET':
        return jsonify(success=True), 200
    if request.method == 'POST':
        file_path = request.form.get('filepath')
        file_name = request.form.get('filename')
        final_name = request.form.get('finalname')
        key = request.form.get('key')  # the key used to encrypt it
        if (file_path is None) or (file_name is None) or (key is None):
            return Response('{"error":"file path, file name and key \
                              must be provided"}',
                            status=422,
                            mimetype='application/json')
        # check if enough memory to read the file
        check_memory_requirement(file_path+file_name)
        # if there is no abort read the file
        target_file = open(file_path+file_name, "r")
        file_data = target_file.read()
        target_file.close()
        # decrypt content
        decrypted_data = decrypt_input_simple(file_data, key)
        # save to drive
        dec_file = open(file_path+final_name, "w")
        dec_file.write(decrypted_data)
        dec_file.close()
        resp = {}
        resp['decryptedFile'] = str(file_path+final_name)
        return Response(json.dumps(resp),
                        status=200,
                        mimetype='application/json')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
