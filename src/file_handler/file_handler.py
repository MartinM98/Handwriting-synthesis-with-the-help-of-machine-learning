import os

class FileHandler(): 
    """
    The class contain all methods that are required to 
    read from, write to and edit a file.
    """

    @classmethod
    def write_to_file(self, file_path, data): 
        """ write data to file, replace content if it exists """

        f = open(file_path, "w")
        f.write(data)
        f.close()

    @classmethod
    def add_to_file(self, file_path, data):
        """ add data to file """

        f = open(file_path, "a")
        f.write(data)
        f.close()

    @classmethod
    def read_from_file(self, file_path):
        """ read data from file """

        f = open(file_path, "r")
        data = f.read()
        f.close()

        return data

    @classmethod
    def create_file(self, file_path, data = None):
        """ read data from file """

        f = open(file_path, "x")
        if data is not None :
            f.write(data)
        f.close()

    @classmethod
    def delete_file(self, file_path):
        """ delete file """

        os.remove(file_path)

    
if __name__ == '__main__':
    FH = FileHandler()
