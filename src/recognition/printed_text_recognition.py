import src.file_handler.file_handler as fh
import os


def take_text(path: str):
    """
    Return text from image.

    Args:
        path (str): Path to image with text.

    Returns:
        str: The text from the image.
    """
    path_without_extention = fh.get_path_without_extention(path)
    command = 'tesseract ' + path + ' ' + \
        path_without_extention + ' -l eng wordstrbox'
    os.system(command)
    boxfilename = path_without_extention + '.box'
    text = ''
    for line in fh.read_from_file_lines(boxfilename):
        words = line.split()
        if words[0] == 'WordStr':
            text += line[line.find('#') + 1:]
    fh.delete_file(boxfilename)
    return text


def take_texts(file_paths: enumerate, TXT_dir: str):
    """
    Read text from images and save them to files.

    Args:
        file_paths (enumerate): Set of path to the images with text.
        TXT_dir (str): Directory where text files are saving.
    """
    for file_path in file_paths:
        name = name = fh.get_file_name(file_path)
        text = take_text(file_path)
        fh.write_to_file(fh.combine_paths(
            TXT_dir, 'TXT_' + name + '.txt'), text)
