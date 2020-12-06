import unittest


class ImageProcessingIntegrationTests(unittest.TestCase):
    """
    The class tests methods from image processing functions.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  Image Processing Integration Tests')

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    Image Processing Integration Tests')

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_integration_image(self):
        pass


if __name__ == '__main__':
    unittest.main()
