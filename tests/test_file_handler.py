import unittest
import os

import src.file_handler.file_handler as fh


class TestFileHandler(unittest.TestCase):
    """
    The class test methods from FileHandler class.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('[START]  FileHandler tests')
        cls.directory = os.path.expanduser('./tmp_tests')
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('[END]    FileHandler tests')
        os.removedirs(cls.directory)

    @classmethod
    def setUp(cls):
        """ before each test """

    def test_create_delete_empty_file(self):
        file_path = os.path.join(self.directory,
                                 'test_create_delete_empty_file.txt')
        fh.create_file(file_path)
        fh.delete_file(file_path)

    def test_create_delete_file_with_content(self):
        file_path = os.path.join(
            self.directory, 'test_create_delete_file_with_content.txt')
        content = 'content'
        fh.create_file(file_path, content)
        result_content = fh.read_from_file(file_path)
        self.assertMultiLineEqual(content, result_content)
        fh.delete_file(file_path)

    def test_create_write_delete(self):
        file_path = os.path.join(
            self.directory, 'test_create_write_delete.txt')
        data = ['content', 'content_2']
        fh.create_file(file_path, data[0])
        fh.write_to_file(file_path, data[1])
        result_content = fh.read_from_file(file_path)
        self.assertMultiLineEqual(data[1], result_content)
        fh.delete_file(file_path)

    def test_create_add_delete(self):
        file_path = os.path.join(
            self.directory, 'test_create_write_delete.txt')
        data = ['content', 'content_2']
        fh.create_file(file_path, data[0])
        fh.add_to_file(file_path, data[1])
        result_content = fh.read_from_file(file_path)
        self.assertMultiLineEqual(''.join(data), result_content)
        fh.delete_file(file_path)


if __name__ == '__main__':
    unittest.main()
