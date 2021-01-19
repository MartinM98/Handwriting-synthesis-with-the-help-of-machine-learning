import cv2
from src.image_processing.common_functions.common_functions import get_dir_and_file
from src.image_processing.common_functions.common_functions import get_parts
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image
from src.image_processing.common_functions.common_functions import resize_and_show_images
import math
import random
import numpy as np


def add_end_points(halves: list, img2: np.ndarray, parts2: list):
    """
    Adds first and last points/pixel to the filtered set of control points.
    Args:
       halves (list): list of selected points/pixels.
       img2 (np.ndarray): image with filtered control points.
       parts2 (list): list of subparts of the initial image that
            that still contains control points.
    """
    if (len(parts2) == 1) and (len(parts2[0]) == 1):
        halves.append(0)
        img2[parts2[0][0][0], parts2[0][0][1]] = 0
        parts2[0].pop(0)
    else:
        halves.append(0)
        rand_index = random.randint(0, len(parts2[0]) - 1)
        img2[parts2[0][rand_index][0], parts2[0][rand_index][1]] = 0
        parts2[0].pop(rand_index)
        halves.append(len(parts2) - 1)
        rand_index = random.randint(0, len(parts2[len(parts2) - 1]) - 1)
        img2[parts2[len(parts2) - 1][rand_index][0], parts2[len(parts2) - 1][rand_index][1]] = 0
        parts2[len(parts2) - 1].pop(rand_index)


def add_point(img2: np.ndarray, tmp: list, halves: list, i: int, parts2: list, offset: int):
    """
    Adds a point to the filtered set of control points.
    Args:
       img2 (np.ndarray): image with filtered control points.
       tmp (list): Copy of the list of selected points/pixels
           into which new point should be inserted.
       halves (list): The list of selected points/pixels.
       i (int): Index of the point that should be inserted.
       parts2 (list): list of subparts of the initial image that
            that still contains control points.
       offset (int): offset in the tmp list (number of previously
       inserted points compared to the halves list)
    """
    mid = math.floor((halves[i + 1] - halves[i]) / 2)
    tmp.insert(i + 1 + offset, halves[i] + mid)
    rand_index = random.randint(
        0, len(parts2[halves[i] + mid]) - 1)
    img2[parts2[halves[i] + mid][rand_index][0],
         parts2[halves[i] + mid][rand_index][1]] = 0
    parts2[halves[i] + mid].pop(rand_index)


def filter_points(img2: np.ndarray, parts: list, n: int):
    """
    Main filtering function that saves the filtered
    points/pixels in the img2 cv2 image.
    Args:
       img2 (np.ndarray): image with filtered control points.
       parts (list): list of subparts of the initial image.
       n (int): the number of subparts in each direction.
    """
    parts2 = [part for part in parts if len(part) > 0]
    halves = []
    if n == 1:
        rand_index = random.randint(
            0, len(parts2[0]) - 1)
        img2[parts2[0][rand_index][0], parts2[0][rand_index][1]] = 0
        return
    state = 2
    while(state < n):
        parts2 = [part for part in parts2 if len(part) > 0]
        if len(parts2) == 0:
            return
        halves = []
        add_end_points(halves, img2, parts2)
        while(len(halves) < n and len(halves) < len(parts2)):
            tmp = halves.copy()
            offset = 0
            for i in range(0, len(halves) - 1):
                if halves[i] == (halves[i + 1] - 1):
                    continue
                add_point(img2, tmp, halves, i, parts2, offset)
                offset += 1
                state += 1
                if(state == n):
                    break
            halves = tmp
            if(state == n):
                break


def binary_search_filter(img: np.ndarray = None, n: int = -1, k: int = -1):
    """
    Creates the subparts, filters the control points, shows the
    results and saves the result.

    Args:
        img (np.darray): image with control points that should be filtered.
        n (int, optional): a scalar determining number of
        subparts of the image. The image is divided into
        n x n subparts with equal sizes.
        k (int, optional): the number of points that should be selected.

    Returns:
        img2 (np.darray): The image with filtered control points.
    """
    if (n < 1) or (k < 1):
        return prepare_blank_image(img.shape)

    save = False
    if img is None:
        directory, path2, path = get_dir_and_file()
        img = get_image(path)
        save = True

    parts = []
    get_parts(img, n, parts)

    img2 = prepare_blank_image(img.shape)
    filter_points(img2, parts, k)
    if save:
        resize_and_show_images(img, img2)
        cv2.imwrite(directory + '/' + path2 + '_bs.png', img2)

    return img2


if __name__ == '__main__':
    binary_search_filter()
