import unittest

from tests.unit_tests.unit_test_file_handler import FileHandlerUnitTests
from tests.unit_tests.unit_test_recognition import RecognitionUnitTests
from tests.unit_tests.unit_test_synthesis import SynthesisUnitTests
from tests.unit_tests.unit_test_image_processing import ImageProcessingUnitTests
from tests.integration_tests.integration_test_file_handler import FileHandlerIntegrationTests
from tests.integration_tests.integration_test_synthesis import SynthesisIntegrationTests
from tests.integration_tests.integration_test_recognition import RecognitionIntegrationTests
from tests.integration_tests.integration_test_image_processing import ImageProcessingIntegrationTests


def run_listed_tests():
    """
    Run all test lited below.
    """

    # set of test classes
    test_classes_to_run = [FileHandlerUnitTests, ImageProcessingUnitTests,
                           SynthesisUnitTests, RecognitionUnitTests,
                           FileHandlerIntegrationTests, ImageProcessingIntegrationTests,
                           SynthesisIntegrationTests, RecognitionIntegrationTests]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    test_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    runner.run(test_suite)


def run_all_tests():  # run all test
    """
    Run all test.
    """

    loader = unittest.TestLoader()
    unit_test_suite = loader.discover('tests', pattern='*unit_test*.py')
    integration_test_suite = loader.discover(
        'tests', pattern='*integration_test*.py')
    runner = unittest.TextTestRunner()
    runner.run(unit_test_suite)
    runner.run(integration_test_suite)


if __name__ == '__main__':
    run_all_tests()
    # run_listed_tests()
