import unittest

from src.handwriting_recognition.handwriting_recognition import HandwritingRecognition

class TestHandwritingRecognition(unittest.TestCase):
    """
    The class test methods from HandwritingRecognition class.
    """


    @classmethod
    def setUpClass(self):
        """ before all tests """

        print("[START]  HandwritingRecognition tests")


    @classmethod
    def tearDownClass(self):
        """ after all tests """

        print("[END]    HandwritingRecognition tests")


    @classmethod
    def setUp(self):
        """ before each test """

        self.HR = HandwritingRecognition()  


    @classmethod
    def tearDown(self):
        """ after each test """

        pass


    def test_foo(self): 
        """ test of the first method """

        self.assertTrue(self.HR.foo())


    def test_foo2(self):
        """ test of the second method """

        self.assertFalse(self.HR.foo2())


    def test_foo3(self):
        """ test of the third method """

        pass


if __name__ == '__main__':
    unittest.main()
