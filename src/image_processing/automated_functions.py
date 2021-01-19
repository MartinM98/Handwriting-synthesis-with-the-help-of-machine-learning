import os
from src.synthesis.control_points import produce_bspline
import cv2
import random
import numpy as np
import unidecode
from src.file_handler.file_handler import combine_paths, ensure_create_dir, get_filename_without_extention
from src.image_processing.skeletonize import skeletonize_image
from src.image_processing.gabor_filter import gabor_filter
from src.graphical_interface.model_dialog import ModelDialog
from src.image_processing.consecutive_filter import consecutive
from src.image_processing.random_filter import random_filter
from src.image_processing.binary_search_filter import binary_search_filter
from src.image_processing.common_functions.common_functions import is_int
from src.image_processing.resize import resize_image
from src.image_processing.common_functions.common_functions import prepare_blank_image, get_dir


def create_skeletons_and_control_points(directory: str):
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


def prepare_images(path_skeleton: str, path_control_points: str, path_control_points2: str, n: int, k: int, option: str):
    """
    Prepares images for letter generation. Filters control points based on the option.

    Args:
       path_skeleton (str): Path to the image with skeleton of the base letter.
       path_skeleton (str): Path to the image with control points of the base letter.
       path_skeleton (str): Path to the image with control points of the second letter.
       n (int): a scalar determining number of
            subparts of the image. The image is divided into
            n x n subparts with equal sizes.
       k (int): the number of points that should be selected.
       option (str): Option describing the filtering.

    Returns:
        (np.ndarray): Image with skeleton of the base letter.
        (np.ndarray): Image with filtered control points of the base letter.
        (np.ndarray): Image with filtered control points of the second letter.
    """
    image = cv2.imread(path_skeleton)
    image = cv2.rotate(image, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points = cv2.imread(path_control_points)
    image_control_points = cv2.rotate(
        image_control_points, cv2.cv2.ROTATE_90_CLOCKWISE)
    image_control_points2 = cv2.imread(path_control_points2)
    image_control_points2 = cv2.rotate(
        image_control_points2, cv2.cv2.ROTATE_90_CLOCKWISE)
    if (n > 0) and (k > 0):
        image_control_points = filter_image(image_control_points, option, n, k)
        image_control_points2 = filter_image(
            image_control_points2, option, n, k)
    return image, image_control_points, image_control_points2


def filter_image(image: np.ndarray, option: str, n: int, k: int):
    """
    Applies an appropriate filtering of control opints based on the option argument.

    Args:
       image (np.ndarray): Input image with control points.
       option (str): Option describing the filtering.
        n (int): a scalar determining number of
        subparts of the image. The image is divided into
        n x n subparts with equal sizes.
        k (int): the number of points that should be selected.

    Returns:
        (np.ndarray): Filtered image.
    """
    image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if option == 'Original':
        return image
    if option == 'Consecutive':
        return consecutive(image2, n, k)
    if option == 'Random':
        return random_filter(image2, n, k)
    if option == 'BS':
        return binary_search_filter(image2, n, k)


def prepare_letters(input: str, path: str, n_advanced_options: int, k_advanced_options: int, option: str, font_size: int, match_with_other: bool):
    """
    Prepares and saves b-splines for given input string in the appropriate directory.

    Args:
       input (str): String for which the b-splines have to be generated.
       path (str): Path to the dataset
       n_advanced_options (int): a scalar determining number of
            subparts of the image. The image is divided into
            n x n subparts with equal sizes.
       k_advanced_options (int): the number of points that should be selected.
       option (str): Option of filtering.
       font_size (int): Size of the font.
       match_with_other (bool): a flag indicating if letters should be matched with eachother
    """
    i = 0
    for letter in input:
        letter = unidecode.unidecode(letter)
        if ord(letter) == 32:
            blank = prepare_blank_image((font_size, font_size * 3))
            cv2.imwrite(
                f"{'./data/synthesis/synthesized/'}/{str(i)}.png", blank)
            i += 1
            continue
        if ord(letter) == 10:
            blank = prepare_blank_image((1, 1))
            cv2.imwrite(
                f"{'./data/synthesis/synthesized/'}/{str(i)}.png", blank)
            i += 1
            continue
        dir = letter
        if letter.islower():
            dir = letter + '2'
        elif not os.path.isdir(path + '/' + dir):
            print('There is no instance of letter ', letter)
            print('Looking for lowercase ', letter)
            dir = letter + '2'
            letter = letter.lower()
        dir_skel = path + '/' + dir + '/skel/'
        dir_filtered = path + '/' + dir + '/filtered/'
        dir_destination = './data/synthesis/skeletons/'
        if not os.path.isdir(path + '/' + dir):
            print('There is no instance of letter ', letter)
            i += 1
            continue
        length = len(
            [filename for filename in os.listdir(path + '/' + dir) if filename.endswith('.png')]) - 1
        if length == -1:
            print('There is no instance of letter ', letter)
            i += 1
            continue
        if length == 0:
            image = resize_image(
                '', 256, 256, image=cv2.imread(dir_skel + '0.png'))
            cv2.imwrite(f"{dir_destination}/{str(i)}.png", image)
            i += 1
            continue
        files = [filename for filename in os.listdir(dir_skel)]
        idx1 = random.randint(0, length)
        idx2 = idx1
        while idx1 == idx2:
            idx2 = random.randint(0, length)
        image, image_control_points, image_control_points2 = prepare_images(
            dir_skel + files[idx1], dir_filtered + files[idx1], dir_filtered + files[idx2], n_advanced_options, k_advanced_options, option)
        produce_bspline(image=image, image_control_points=image_control_points,
                        image_control_points2=image_control_points2, idx=i, match_with_other=match_with_other)
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

    create_skeletons_and_control_points(directory=directory)
