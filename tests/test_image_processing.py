import unittest


class ImageProcessingTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('[START]  Image Processing Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('[END]    Image Processing Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_name(self):
        pass


if __name__ == '__main__':
    unittest.main()
