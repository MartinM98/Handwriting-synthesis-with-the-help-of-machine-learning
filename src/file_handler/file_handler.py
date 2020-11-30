import os


def write_to_file(file_path: str, data: str):
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


def add_to_file(file_path: str, data: str):
    """
    Add data to file.

    Args:
        file_path (str): Path to the file.
        data (str): Data to add to the file.
    """
    f = open(file_path, "a")
    f.write(data)
    f.close()


def read_from_file(file_path: str):
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


def read_from_file_lines(file_path: str):
    """
    Read data as lines from file.

    Args:
        file_path (str): Path to the file.

    Returns:
        str: The line data from the file.
    """
    f = open(file_path, "r")
    lines = f.readlines()
    f.close()

    return lines


def create_file(file_path: str, data: str = None):
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


def delete_file(file_path: str):
    """
    Delete the file.

    Args:
        file_path (str): Path to the file.
    """
    os.remove(file_path)


def ensure_create_dir(dir_path: str):
    """
    Create directory if such does not exit.

    Args:
        file_path (str): Path to new directory.
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_absolute_path(realtive_path: str):
    """
    Return absolute path from relative one.

    Args:
        realtive_path (str): Relative path.

    Returns:
        str: Absolute path.
    """
    return os.path.abspath(realtive_path)


def get_relative_path(absolute_path: str):
    """
    Retrun relative path from absolute one.

    Args:
        absolute_path (str): Absolute path.

    Returns:
        str: Relative path.
    """
    current_dir = get_current_path()
    return os.path.relpath(absolute_path, current_dir)


def combine_paths(first_path: str, second_path: str):
    """
    Retrun combined paths.

    Args:
        first_path (str): First part of path.
        second_path (str): Second part of path.

    Returns:
        str: Combined path.
    """
    return os.path.join(first_path, second_path)


def get_current_path():
    """
    Retrun current path.

    Returns:
        str: Current path.
    """
    return os.path.abspath(os.getcwd())


def get_file_name(file_path: str):
    """
    Retrun file name.

    Returns:
        str: File name.
    """
    return os.path.basename(file_path)


def get_dir_path(file_path: str):
    """
    Retrun directory path.

    Returns:
        str: Directory path.
    """
    return os.path.dirname(file_path)


def get_dir_path(file_path: str):
    """
    Retrun directory path.
    Returns:
        str: Directory path.
    """
    return os.path.dirname(file_path)


def get_path_without_extention(file_path: str):
    """
    Retrun path without extention of the file.

    Returns:
        str: Path without extention.
    """
    return os.path.splitext(file_path)[0]
