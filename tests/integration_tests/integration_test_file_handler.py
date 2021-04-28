import unittest
import os

import src.file_handler.file_handler as fh


class FileHandlerIntegrationTests(unittest.TestCase):
    """
    The class tests methods from FileHandler class.
    """

    @classmethod
    def setUpClass(cls):
        """ before all tests """
        print('\n[START]  File Handler Integration Tests')
        cls.directory = os.path.expanduser('./tmp_tests')
        if not os.path.exists(cls.directory):
            os.makedirs(cls.directory)

    @classmethod
    def tearDownClass(cls):
        """ after all tests """
        print('\n[END]    File Handler Integration Tests')
        fh.remove_dir_with_content(cls.directory)

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

    def test_ensure_create_and_append_file(self):
        file_path = os.path.join(
            self.directory, 'test_ensure_create_and_append_file.txt')
        data = ['content', 'content_2']
        fh.ensure_create_and_append_file(file_path, data[0])
        result_content = fh.read_from_file(file_path)
        self.assertMultiLineEqual(''.join(data[0]), result_content)
        fh.ensure_create_and_append_file(file_path, data[1])
        result_content = fh.read_from_file(file_path)
        self.assertMultiLineEqual(''.join(data), result_content)
        fh.delete_file(file_path)

    def test_ensure_remove_file(self):
        file_path = os.path.join(
            self.directory, 'test_ensure_remove_file.txt')
        self.assertFalse(os.path.isfile(file_path))
        fh.ensure_remove_file(file_path)
        data = ['content']
        fh.create_file(file_path, data[0])
        self.assertTrue(os.path.isfile(file_path))
        fh.ensure_remove_file(file_path)
        self.assertFalse(os.path.isfile(file_path))

    def test_read_from_file_lines(self):
        file_path = os.path.join(
            self.directory, 'test_read_from_file_lines.txt')
        data = ['content\n', 'content_2']
        fh.create_file(file_path, data[0])
        fh.add_to_file(file_path, data[1])
        result_content = fh.read_from_file_lines(file_path)
        self.assertEqual(len(result_content), len(data))
        self.assertEqual(result_content[0], data[0])
        self.assertEqual(result_content[1], data[1])
        fh.delete_file(file_path)

    def test_ensure_create_dir(self):
        dir_path = os.path.join(
            self.directory, 'test_ensure_create_dir')
        self.assertFalse(os.path.exists(dir_path))
        fh.ensure_create_dir(dir_path)
        self.assertTrue(os.path.exists(dir_path))
        fh.ensure_create_dir(dir_path)
        self.assertTrue(os.path.exists(dir_path))
        fh.remove_dir_with_content(dir_path)


if __name__ == '__main__':
    unittest.main()
