import src.file_handler.file_handler as fh
import xml.etree.ElementTree as ET
import multiprocessing
from glob import glob


def read_xml(path_to_xml_file: str):
    """
    The funtion reads the xml file and returns list of text atrribute from the line elements.
    It is prepared only for xml from the dataset.

    Args:
        path_to_xml_file (str): Path to the xml file.

    Returns:
        (list): List of proper readed lines from the dataset.
    """
    tree = ET.parse(path_to_xml_file)
    root = tree.getroot()
    lines = list()
    for child in root.findall("./handwritten-part/line"):
        lines.append(child.attrib['text'])
    return lines


def postproduce(path_to_box_file: str):
    """
    Fixing of the lines from the box file.
    Repleace the lines with the propren one from the xml files from the dataset.

    Args:
        path_to_box_file (str): Path to the box file, which will be changed.
    """
    # remove prefix 'HT_'
    name = fh.get_file_name(path_to_box_file)[3:]
    path_to_xml_files = fh.get_absolute_path('./data/xml/')
    xml_lines = read_xml(fh.combine_paths(path_to_xml_files, name + '.xml'))

    # read lines from box and replacing
    new_lines = list()
    with open(path_to_box_file, 'r', encoding="utf8") as box_file:
        box_lines = box_file.readlines()
        counter = 0
        for line in box_lines:
            line_parts = line.rstrip().split('#')
            if '#' in line and line_parts[1]:
                if counter < len(xml_lines):
                    line = line_parts[0] + '#' + xml_lines[counter] + '\n'
                else:
                    line = line_parts[0] + '#' + '\n'
                counter += 1
            new_lines.append(line)

    # saving the proper file
    with open(path_to_box_file, "w") as box_file:
        box_file.writelines(new_lines)


def postproduce_set(path_to_dataset: str):
    """
    For every box file from the path is running the the postproduce process.
    The function using multiproccesing is fixing the files in the path.

    Args:
        path_to_dataset (str): Path to the set of box files.
    """
    dir_path = fh.combine_paths(path_to_dataset, '*.box')
    iterable = [file for file in glob(dir_path)]

    p = multiprocessing.Pool()
    p.map_async(postproduce, iterable)

    p.close()
    p.join()


if __name__ == '__main__':
    path_to_dataset = fh.get_absolute_path('./tesseract-training/hardware-dependent/windows/')
    postproduce_set(path_to_dataset)
