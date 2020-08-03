import unittest

from test_handwriting_recognition import TestHandwritingRecognition

def run_all_tests(): # run all test lited below
    test_classes_to_run = [TestHandwritingRecognition] # set of test classes

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)
        
    test_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    runner.run(test_suite)

if __name__ == '__main__':
    run_all_tests() 
    