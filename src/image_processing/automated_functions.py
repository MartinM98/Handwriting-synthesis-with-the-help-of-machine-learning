import matplotlib.pyplot as plt
import os
import cv2
import random
import numpy as np
from src.file_handler.file_handler import combine_paths, ensure_create_dir
from src.image_processing.skeletonize import skeletonize_image
from src.file_handler.file_handler import get_filename_without_extention
from src.image_processing.common_functions.common_functions import get_dir
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.gabor_filter import gabor_filter
from src.synthesis.control_points import produce_imitation, produce_bspline
from src.graphical_interface.load_dialog import LoadDialog
from src.graphical_interface.model_dialog import ModelDialog
from src.image_processing.consecutive_filter import consecutive
from src.image_processing.random_filter import random_filter
from src.image_processing.binary_search_filter import binary_search_filter
from src.image_processing.common_functions.common_functions import is_int
from src.file_handler.file_handler import get_absolute_path


def gabor_filter_automated(directory: str = None):
    """
    Applies the gabor filter with given paramters to
    all images with the extension png in the selected directory and
    saves the results.

    Args:
       directory (str, optional): the path to the directory that should
       be processed.

    Returns:
        list: The list of filtered images.
    """
    save = False
    if directory is None:
        directory = get_dir()
        save = True

    results = []

    for entry in os.scandir(directory):
        if (entry.path.endswith("_skel.png")):
            path2 = get_filename_without_extention(entry.path)
            path = entry.path
            result = gabor_filter(get_image(path))
            if save:
                cv2.imwrite(directory + '/' + path2 + '_control_points.png',
                            result)
            results.append(result)

    return results


def skeletonize_automated(directory: str = None):
    """
    Skeletonizes all images with the extension png in the selected directory and
    saves the results.

    Args:
       directory (str, optional): the path to the directory that should
       be processed.

    Returns:
        list: The list of skeletonized images.
    """
    save = False
    if directory is None:
        directory = get_dir()
        save = True

    results = []

    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = get_filename_without_extention(entry.path)
            path = entry.path
            img = skeletonize_image(path=path)
            if save:
                plt.imsave(directory + '/' + path2 + '_skel.png',
                           img, cmap=plt.cm.gray)
            results.append(img)

    return results


def create_skeletons_and_control_points(directory: str, options: list = None):
    """
    Applies skeletonization and gabor filter to the given dataset
    with the standard structure.

    Args:
       directory (str): the path to the directory that should
       be processed.
    """
    for dir in sorted(os.listdir(directory)):
        if not dir.startswith('.'):
            dir2 = directory + '/' + dir + '/'
            dir3 = directory + '/' + dir + '/skel/'
            dir4 = directory + '/' + dir + '/filtered/'
            ensure_create_dir(dir3)
            ensure_create_dir(dir4)
            for file in sorted(os.listdir(dir2)):
                if file.endswith('.png'):
                    filename = get_filename_without_extention(file)
                    path = combine_paths(dir2, file)
                    img = cv2.imread(path)
                    skeleton = skeletonize_image(img)
                    cv2.imwrite(dir3 + filename + '.png', skeleton)
                    gabor = gabor_filter(path=dir3 + filename + '.png')
                    cv2.imwrite(dir4 + filename + '.png', gabor)
                    filter_points_based_on_options(gabor, options, dir4 + filename)


def create_bsplines(directory: str, options: list = None):
    """
    Generates letters in the given dataset
    with the standard structure.

    Args:
       directory (str): the path to the directory that should
       be processed.
    """
    for dir in sorted(os.listdir(directory)):
        if not dir.startswith('.'):
            dir3 = directory + '/' + dir + '/skel/'
            dir4 = directory + '/' + dir + '/filtered/'
            length = len(
                [filename for filename in os.listdir(directory + '/' + dir) if filename.endswith('.png')]) - 1
            if length < 1 or dir == 'dot':
                continue
            ensure_create_dir(directory + '/' + dir + '/bspline/')
            files = [filename for filename in os.listdir(
                dir3)]
            for i in range(len(files)):
                idx = i
                while idx == i:
                    idx = random.randint(0, length)
                produce_imitation(
                    path_to_skeleton=dir3 + files[i], path_to_control_points=dir4 + files[i], path_to_control_points2=dir4 + files[idx], idx=idx)


def filter_points_based_on_options(gabor: np.ndarray, options: list, path: str):
    """
    Filters control points based on options.

    Args:
        gabor (np.ndarray): image with control points.
        options (list): list of options.
        path (str): path to the destination of the images.
    """
    if len(options) > 0:
        if (options[0] is not None) and (options[1] is not None):
            try_filter_points_consecutive(gabor, path, options[0], options[1])

        if (options[2] is not None) and (options[3] is not None):
            try_filter_points_random(gabor, path, options[2], options[3])

        if (options[4] is not None) and (options[5] is not None):
            try_filter_points_bs(gabor, path, options[4], options[5])


def try_filter_points_consecutive(gabor: np.ndarray, path: str, n: int, k: int):
    """
    Tries to apply consecutive filter on a image with control points.

    Args:
        gabor (np.ndarray): image with control points.
        path (str): path to the destination of the images.
        n (int,): a scalar determining number of
        subparts of the image. The image is divided into
        n x n subparts with equal sizes.
        k (int): the number of points that should be selected.
    """
    try:
        c = consecutive(gabor, n, k)
        cv2.imwrite(path + '_c.png', c)
    except ValueError:
        print('Consecutive filter error (', path + '_c.png')


def try_filter_points_random(gabor: np.ndarray, path: str, n: int, k: int):
    """
    Tries to apply random filter on a image with control points.

    Args:
        gabor (np.ndarray): image with control points.
        path (str): path to the destination of the images.
        n (int,): a scalar determining number of
        subparts of the image. The image is divided into
        n x n subparts with equal sizes.
        k (int): the number of points that should be selected.
    """
    try:
        r = random_filter(gabor, n, k)
        cv2.imwrite(path + '_r.png', r)
    except ValueError:
        print('Random filter error (', path + '_r.png')


def try_filter_points_bs(gabor: np.ndarray, path: str, n: int, k: int):
    """
    Tries to apply binary search filter on a image with control points.

    Args:
        gabor (np.ndarray): image with control points.
        path (str): path to the destination of the images.
        n (int,): a scalar determining number of
        subparts of the image. The image is divided into
        n x n subparts with equal sizes.
        k (int): the number of points that should be selected.
    """
    try:
        bs = binary_search_filter(gabor, n, k)
        cv2.imwrite(path + '_bs.png', bs)
    except ValueError:
        print('BS error error (', path + '_bs.png')


def process_options(ld: LoadDialog):
    """
    Creates a list of options in the advanced mode of load process.

    Args:
       directory (LoadDialog): Instance of custom class LoadDialog.

    Returns:
        list : list of options retrieved from the LoadDialog class
    """
    options = []
    if is_int(ld.consecutive_n.GetValue()):
        options.append(int(ld.consecutive_n.GetValue()))
    else:
        options.append(None)

    if is_int(ld.consecutive_k.GetValue()):
        options.append(int(ld.consecutive_k.GetValue()))
    else:
        options.append(None)

    if is_int(ld.random_n.GetValue()):
        options.append(int(ld.random_n.GetValue()))
    else:
        options.append(None)

    if is_int(ld.random_k.GetValue()):
        options.append(int(ld.random_k.GetValue()))
    else:
        options.append(None)

    if is_int(ld.bs_n.GetValue()):
        options.append(int(ld.bs_n.GetValue()))
    else:
        options.append(None)

    if is_int(ld.bs_k.GetValue()):
        options.append(int(ld.bs_k.GetValue()))
    else:
        options.append(None)

    return options


def prepare_letters(input: str):
    """
    Prepares and saves b-splines for given input string in the appropriate directory.

    Args:
       input (str): the string for which the b-splines have to be generated.
    """
    i = 0
    for letter in input:
        dir = letter
        if letter.islower():
            dir = letter + '2'
        dir_dataset = get_absolute_path('./src/graphical_interface/letters_dataset/')
        dir_skel = dir_dataset + '/' + dir + '/skel/'
        dir_filtered = dir_dataset + '/' + dir + '/filtered/'
        dir_destination = get_absolute_path('./src/graphical_interface/synthesis/skeletons/')
        if not os.path.isdir(dir_dataset + '/' + dir):
            print('There is no instance of letter ', letter)
            i += 1
            continue
        length = len(
            [filename for filename in os.listdir(dir_dataset + '/' + dir) if filename.endswith('.png')]) - 1
        if length == 0:
            image = cv2.imread(dir_skel + '0.png')
            cv2.imwrite(f"{dir_destination}{str(i)}.png", image)
            i += 1
            continue
        files = [filename for filename in os.listdir(dir_skel)]
        idx1 = random.randint(0, length)
        idx2 = idx1
        while idx1 == idx2:
            idx2 = random.randint(0, length)
        produce_bspline(path_to_skeleton=dir_skel + files[idx1], path_to_control_points=dir_filtered + files[idx1], path_to_control_points2=dir_filtered + files[idx2], idx=i)
        i += 1


def process_model_options(md: ModelDialog):
    """
    Creates a list of options for the model.

    Args:
       directory (ModelDialog): Instance of custom class ModelDialog.

    Returns:
        list : list of options retrieved from the ModelDialog class
    """
    options = []
    if is_int(md.epochs.GetValue()):
        options.append(int(md.epochs.GetValue()))
    else:
        options.append(None)

    if is_int(md.ngf.GetValue()):
        options.append(int(md.ngf.GetValue()))
    else:
        options.append(None)

    if is_int(md.ndf.GetValue()):
        options.append(int(md.ndf.GetValue()))
    else:
        options.append(None)

    return options


def process_dataset(directory: str = None, options: list = None):
    """
    Invokes functions applying skeletonization, gabor filter
    and generate letters to the given dataset with the standard structure.

    Args:
       directory (str, optional): the path to the directory that should
       be processed.
    """
    if directory is None:
        directory = get_dir()

    create_skeletons_and_control_points(directory=directory, options=options)
    create_bsplines(directory=directory, options=options)


if __name__ == "__main__":
    process_dataset()
