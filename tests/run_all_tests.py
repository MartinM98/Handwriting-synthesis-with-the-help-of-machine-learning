from os import removedirs
import unittest
from datetime import datetime

from tests.unit_tests.unit_test_file_handler import FileHandlerUnitTests
from tests.unit_tests.unit_test_recognition import RecognitionUnitTests
from tests.unit_tests.unit_test_synthesis import SynthesisUnitTests
from tests.unit_tests.unit_test_image_processing import ImageProcessingUnitTests
from tests.integration_tests.integration_test_file_handler import FileHandlerIntegrationTests
from tests.integration_tests.integration_test_synthesis import SynthesisIntegrationTests
from tests.integration_tests.integration_test_recognition import RecognitionIntegrationTests
from tests.integration_tests.integration_test_image_processing import ImageProcessingIntegrationTests
from src.file_handler.file_handler import combine_paths, ensure_create_and_append_file, ensure_create_dir, get_absolute_path, remove_dir_with_content


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


def run_all_tests():
    """
    Run all test.
    """

    loader = unittest.TestLoader()
    unit_test_suite = loader.discover('tests', pattern='*unit_test*.py')
    integration_test_suite = loader.discover(
        'tests', pattern='*integration_test*.py')
    runner = unittest.TextTestRunner(verbosity=3)
    unit_test_result = runner.run(unit_test_suite)
    integration_test_result = runner.run(integration_test_suite)
    log_errors(unit_test_result, integration_test_result)


def log_errors(unit_test_result: list, integration_test_result: list):
    """
    Function analyse results of tests and log failed to file.

    Args:
        unit_test_result (list): Results of unit tests.
        integration_test_result (list): Results of integration tests.
    """
    n_failed = len(unit_test_result.failures) + \
        len(integration_test_result.failures)
    if n_failed > 0:
        path = get_absolute_path('./tests/logs/')
        ensure_create_dir(path)
        now = datetime.now()
        dt_string = now.strftime('%d_%m_%Y_%H_%M_%S')
        file_name = 'logs_' + dt_string + '.txt'
        path = combine_paths(path, file_name)
        data = 'Tests erros from date: ' + \
            now.strftime('%d/%m/%Y %H:%M:%S') + '.\n\n'
        data += 'Unit Tests\n\n'
        for fail in unit_test_result.failures:
            data += '--------------------------\n'
            for f in fail:
                data += str(f) + '\n\n'
        data += 'Integration Tests\n\n'
        for fail in integration_test_result.failures:
            data += '--------------------------\n'
            for f in fail:
                data += str(f) + '\n\n'
        ensure_create_and_append_file(path, data)


if __name__ == '__main__':
    run_all_tests()
    # run_listed_tests()
    path_to_output = get_absolute_path('./tests/data/output')
    remove_dir_with_content(path_to_output)
