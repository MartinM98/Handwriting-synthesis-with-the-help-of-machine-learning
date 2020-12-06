import unittest
import os


class FileHandlerUnitTests(unittest.TestCase):
    """
    The class tests methods from FileHandler class.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  File Handler Unit Tests')
        cls.directory = os.path.expanduser('./tmp_tests')
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    File Handler Unit Tests')
        os.removedirs(cls.directory)

    @classmethod
    def setUp(cls):
        """ before each test """


if __name__ == '__main__':
    unittest.main()
