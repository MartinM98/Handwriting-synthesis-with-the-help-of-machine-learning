import cv2
from src.image_processing.common_functions.common_functions import get_dir_and_file
from src.image_processing.common_functions.common_functions import get_parts
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image
from src.image_processing.common_functions.common_functions import resize_and_show_images
import sys
import numpy as np
import random


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
    checked = np.zeros(len(parts2))
    n_checked = 0
    index = random.randint(0, len(checked) - 1 - n_checked)

    while(n > 0):
        if len(parts2[index]) != 0:
            rand_index = random.randint(0, len(parts2[index]) - 1)
            img2[parts2[index][rand_index][0],
                 parts2[index][rand_index][1]] = 0
            parts2[index].pop(rand_index)
            n -= 1
        else:
            min_index = parts.index(max(parts, key=lambda part: len(part)))
            if len(parts[min_index]) == 0:
                break
        checked[index] = 1
        n_checked += 1
        if n_checked == len(checked):
            checked = np.zeros(len(checked))
        n_checked = n_checked % len(checked)
        index = random.randint(0, len(checked) - 1 - n_checked)
        i = 0
        temp = 0
        while(checked[temp] == 1):
            temp += 1
        while(i < index):
            if checked[temp] == 0:
                i += 1
            temp += 1
        index = temp


def random_filter():
    """
    Creates the subparts, filters the control points, shows the
    results and saves the result.
    Args:
        None
    """
    if len(sys.argv) == 1:
        exit()
    n = int(sys.argv[1])

    directory, path2, path = get_dir_and_file()

    img = get_image(path)

    parts = []
    get_parts(img, n, parts)

    if len(sys.argv) == 2:
        exit()

    n = int(sys.argv[2])

    img2 = prepare_blank_image(img)
    filter_points(img2, parts, n)
    resize_and_show_images(img, img2)
    cv2.imwrite(directory + '/' + path2 + '_filtered.png', img2)


if __name__ == '__main__':
    random_filter()
