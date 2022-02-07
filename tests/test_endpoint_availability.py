# -*- coding: utf-8 -*-
'''
testing that all endpoints are available
'''
import unittest
import requests


class TestEndpoints(unittest.TestCase):
    '''
    Test get functionality of all endoints
    '''
    def test_verify_server(self):
        '''
        Test that the server is running
        '''
        response = requests.get('http://127.0.0.1:5000/check')
        self.assertEqual(200, response.status_code)

    def test_verify_encrypt_data(self):
        '''
        Test that encrypt data is available
        '''
        response = requests.get('http://127.0.0.1:5000/encrypt-data/simple')
        self.assertEqual(200, response.status_code)

    def test_verify_decrypt_data(self):
        '''
        Test that decrypt data is available
        '''
        response = requests.get('http://127.0.0.1:5000/decrypt-data/simple')
        self.assertEqual(200, response.status_code)

    def test_verify_encrypt_file(self):
        '''
        Test that encrypt file is available
        '''
        response = requests.get('http://127.0.0.1:5000/encrypt-file')
        self.assertEqual(200, response.status_code)

    def test_verify_decrypt_file(self):
        '''
        Test that decrypt file is available
        '''
        response = requests.get('http://127.0.0.1:5000/decrypt-file')
        self.assertEqual(200, response.status_code)
