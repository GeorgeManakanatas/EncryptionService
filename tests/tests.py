# -*- coding: utf-8 -*-
'''
Central unit testing
'''
import unittest
from . import test_encrypt_decrypt_data, test_endpoint_availability


def main():
    '''
    Main unit test routine. The test suite is built here and then run
    '''
    # create loader and suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    # will probably need a loop here after a wile
    suite.addTests(loader.loadTestsFromModule(test_endpoint_availability))
    suite.addTests(loader.loadTestsFromModule(test_encrypt_decrypt_data))
    # set runner and run tests
    runner = unittest.TextTestRunner(verbosity=2)
    return runner.run(suite)


if __name__ == '__main__':
    main()
