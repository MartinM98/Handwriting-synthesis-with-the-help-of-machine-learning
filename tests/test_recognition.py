import unittest


class RecognitionTests(unittest.TestCase):
    """
    The class tests methods from recognition functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Recognition Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Recognition tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_name(self):
        pass


if __name__ == '__main__':
    unittest.main()
