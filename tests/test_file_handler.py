import unittest
import os

from src.file_handler.file_handler import FileHandler

class TestFileHandler(unittest.TestCase):
    """
    The class test methods from FileHandler class.
    """

    @classmethod
    def setUpClass(self):
        """ before all tests """

        print("[START]  FileHandler tests")
        self.directory = os.path.expanduser('./tmp_tests')
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)


    @classmethod
    def tearDownClass(self):
        """ after all tests """

        print("[END]    FileHandler tests")
        os.removedirs(self.directory)


    @classmethod
    def setUp(self):
        """ before each test """

        self.FH = FileHandler()  

    def test_create_delete_empty_file(self): 
        file_path = os.path.join(self.directory, "test_create_delete_empty_file.txt")
        self.FH.create_file(file_path)
        self.FH.delete_file(file_path)

    def test_create_delete_file_with_content(self): 
        file_path = os.path.join(self.directory, "test_create_delete_file_with_content.txt")
        content = "content"
        self.FH.create_file(file_path, content)
        result_content = self.FH.read_from_file(file_path)
        self.assertMultiLineEqual(content, result_content)      
        self.FH.delete_file(file_path)

    def test_create_write_delete(self): 
        file_path = os.path.join(self.directory, "test_create_write_delete.txt")
        data = ["content", "content_2"]
        self.FH.create_file(file_path, data[0])
        self.FH.write_to_file(file_path, data[1])
        result_content = self.FH.read_from_file(file_path)
        self.assertMultiLineEqual(data[1], result_content)      
        self.FH.delete_file(file_path)    

    def test_create_add_delete(self): 
        file_path = os.path.join(self.directory, "test_create_write_delete.txt")
        data = ["content", "content_2"]
        self.FH.create_file(file_path, data[0])
        self.FH.add_to_file(file_path, data[1])
        result_content = self.FH.read_from_file(file_path)
        self.assertMultiLineEqual(''.join(data), result_content)      
        self.FH.delete_file(file_path)  


if __name__ == '__main__':
    unittest.main()
