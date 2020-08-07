import os


class FileHandler():
    """
    The class contain all methods that are required to
    read from, write to and edit a file.
    """

    def write_to_file(self, file_path: str, data: str):
        """
        Write data to file,
        replace content if it exists.

        Args:
            file_path (str): Path to the file.
            data (str): Data to save in the file.
        """
        f = open(file_path, "w")
        f.write(data)
        f.close()

    def add_to_file(self, file_path: str, data: str):
        """
        Add data to file.

        Args:
            file_path (str): Path to the file.
            data (str): Data to add to the file.
        """
        f = open(file_path, "a")
        f.write(data)
        f.close()

    def read_from_file(self, file_path: str):
        """
        Read data from file.

        Args:
            file_path (str): Path to the file.

        Returns:
            str: The data from the file.
        """
        f = open(file_path, "r")
        data = f.read()
        f.close()

        return data

    def create_file(self, file_path: str, data: str = None):
        """
        Create The file.

        Args:
            file_path (str): Path to the file.
            data (str, optional): Data of the new file. Defaults to None.
        """
        f = open(file_path, "x")
        if data is not None:
            f.write(data)
        f.close()

    def delete_file(self, file_path: str):
        """
        Delete the file.

        Args:
            file_path (str): Path to the file.
        """
        os.remove(file_path)


if __name__ == '__main__':
    FH = FileHandler()
