import unittest


class RecognitionIntegrationTests(unittest.TestCase):
    """
    The class tests methods from recognition functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Recognition Integration Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Recognition Integration Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_integration_recognition(self):
        pass


if __name__ == '__main__':
    unittest.main()
