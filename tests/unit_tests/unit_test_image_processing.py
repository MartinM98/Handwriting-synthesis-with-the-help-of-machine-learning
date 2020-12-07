import unittest
from src.image_processing.letters import check_char


class ImageProcessingUnitTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Unit Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Image Processing Unit Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_name(self):
        pass

    def test_check_char(self):
        path = './tests/data'
        lower = check_char(path, 'a')
        upper = check_char(path, 'A')
        colon = check_char(path, ':')
        dot = check_char(path, '.')
        question = check_char(path, '?')
        asterisk = check_char(path, '*')
        self.assertTrue(lower == './tests/data/a2/')
        self.assertTrue(upper == './tests/data/A/')
        self.assertTrue(colon == './tests/data/colon/')
        self.assertTrue(dot == './tests/data/dot/')
        self.assertTrue(question == './tests/data/question/')
        self.assertTrue(asterisk == './tests/data/asterisk/')


if __name__ == '__main__':
    unittest.main()
