import unittest


class ImageProcessingTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Image Processing Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_name(self):
        pass


if __name__ == '__main__':
    unittest.main()
