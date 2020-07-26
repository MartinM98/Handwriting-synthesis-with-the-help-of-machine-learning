import unittest

from src.handwriting_recognition.handwriting_recognition import HandwritingRecognition

class TestHandwritingRecognition(unittest.TestCase):
    '''
    The class test methods from HandwritingRecognition class.
    '''

    HR = HandwritingRecognition()

    def test_foo(self): # test of the first method
        self.assertTrue(self.HR.foo())

    def test_foo2(self): # test of the second method
        self.assertFalse(self.HR.foo2())


if __name__ == '__main__':
    unittest.main()
