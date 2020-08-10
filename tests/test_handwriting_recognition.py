import unittest

from src.handwriting_recognition.handwriting_recognition import (
    HandwritingRecognition
)


class TestHandwritingRecognition(unittest.TestCase):
    """
    The class test methods from HandwritingRecognition class.
    """

    @classmethod
    def setUpClass(cls):
        """
        Before all tests.
        """
        print("[START]  HandwritingRecognition tests")
        cls.HR = HandwritingRecognition()

    @classmethod
    def tearDownClass(cls):
        """
        After all tests.
        """
        print("[END]    HandwritingRecognition tests")

    def test_foo(self):
        """
        Test of the first method.
        """
        self.assertTrue(self.HR.foo())

    def test_foo2(self):
        """
        Test of the second method.
        """
        self.assertFalse(self.HR.foo2())

    def test_foo3(self):
        """
        Test of the third method.
        """
        pass


if __name__ == '__main__':
    unittest.main()
