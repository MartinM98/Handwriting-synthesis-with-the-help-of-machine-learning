import unittest
import os

import src.file_handler.file_handler as fh


class FileHandlerUnitTests(unittest.TestCase):
    """
    The class tests methods from FileHandler class.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  File Handler Unit Tests')
        cls.directory = os.path.expanduser('./tmp_tests')
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    File Handler Unit Tests')
        os.removedirs(cls.directory)

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_get_relative_path(self):
        relative_path = '.\\tests\\smoefile.txt'
        abspath = os.path.abspath(relative_path)
        result = fh.get_relative_path(abspath)
        if result[0] != '.':
            result = '.\\' + result
        self.assertEqual(relative_path, result)

    def test_combine_paths(self):
        path1 = '.\\tests'
        path2 = 'smoefile.txt'
        result = fh.combine_paths(path1, path2)
        self.assertEqual(path1 + os.path.sep + path2, result)
        path3 = '.\\tests\\'
        result = fh.combine_paths(path3, path2)
        self.assertEqual(path3 + path2, result)

    def test_get_current_path(self):
        result = fh.get_current_path()
        self.assertEqual(os.getcwd(), result)

    def test_get_file_name(self):
        path = fh.get_current_path()
        filename = 'txtfile.txt'
        path = fh.combine_paths(path, filename)
        result = fh.get_file_name(path)
        self.assertEqual(filename, result)

    def test_get_dir_path(self):
        path = fh.get_current_path()
        filename = 'txtfile.txt'
        dirname = 'dir'
        dir_path = fh.combine_paths(path, dirname)
        path = fh.combine_paths(path, dirname, filename)
        result = fh.get_dir_path(path)
        self.assertEqual(dir_path, result)

    def test_get_filename_without_extention(self):
        path = fh.get_current_path()
        filename = 'txtfile.txt'
        path = fh.combine_paths(path, filename)
        filename = filename[:-4]
        result = fh.get_filename_without_extention(path)
        self.assertEqual(filename, result)


if __name__ == '__main__':
    unittest.main()
