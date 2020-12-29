import numpy as np
import cv2
import math
import sys
import random


def dist(p1: tuple, p2: tuple):
    """
    Calculates the Euclidean distance between two points.

    Args:
        p1 (tuple): The first point.
        p2 (tuple): The second point.

    Returns:
        (int): floor of the Euclidean distance between two points.
    """
    return math.floor(math.sqrt(math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)))


def mid_point(p1: tuple, p2: tuple):
    """
    Calculates midpoint between two points.

    Args:
        p1 (tuple): The first point.
        p2 (tuple): The second point.

    Returns:
        (tuple): the midpoint between the given two points.
    """
    part = 10
    x = math.floor((p1[0] + p2[0]) / 2)
    y = math.floor((p1[1] + p2[1]) / 2)
    x += x * random.randrange(-part, part + 1) / 100
    y += y * random.randrange(-part, part + 1) / 100
    return (x, y)


def get_shift(p1: list, p2: list):
    """
    Calculates the centroids of two letters and gets the shift between them.

    Args:
        p1 (list): The list of the points of the base letter.
        p2 (list): The list of the points of the second letter.

    Returns:
        (tuple): The tuple representing the shift between the centroids
        of the given two letters.
    """
    x_m = 0
    y_m = 0
    if (len(p1) == 0) or (len(p2) == 0):
        return (0, 0)
    for point in p1:
        x_m += point[0]
        y_m += point[1]
    x_m2 = math.floor(x_m / len(p1))
    y_m2 = math.floor(y_m / len(p1))
    m1 = (x_m2, y_m2)
    x_m = 0
    y_m = 0
    for point in p2:
        x_m += point[0]
        y_m += point[1]
    x_m2 = math.floor(x_m / len(p2))
    y_m2 = math.floor(y_m / len(p2))
    m2 = (x_m2, y_m2)
    m3 = (m2[0] - m1[0], m2[1] - m1[1])
    return m3


def shift_points(p: list, m3: tuple):
    """
    Shifts points of a letter by the given tuple.

    Args:
        p (list): The list of the points of a letter.
        m3 (tuple): The list of the points of the second letter.

    Returns:
        (list): Shifted points of the inputed letter.
    """
    p2 = []
    for i in p:
        p2.append((i[0] - m3[0], i[1] - m3[1]))
    return p2


def generate_points(p1: list, p2: list):
    """
    Generates points of a letter based on the inputted two lists of points.
    The new points are computed as midpoints between all points from the
    first list and the nearest point to it from the second list.

    Args:
        p1 (list): The list of the points of the base letter.
        p2 (tuple): The list of the points of the second letter.

    Returns:
        (list): List of points of the generated letter.
    """
    p3 = []
    for point in p1:
        d = sys.maxsize
        p_tmp = (0, 0)
        for point2 in p2:
            tmp = dist(point, point2)
            if tmp < d:
                d = tmp
                p_tmp = point2
        p3.append((point, mid_point(point, p_tmp)))
    return p3


def generate_letter(img1: np.ndarray, img2: np.ndarray):
    """
    Main function generating a new letter.

    Args:
        path (str): The path to the base letter.
        path2 (str): The path to the second letter.

    Returns:
        (list): List of points of the generated letter.
    """
    if len(img1.shape) == 3:
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    if len(img2.shape) == 3:
        img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    l1 = []
    for ix, iy in np.ndindex(img1.shape):
        if(img1[ix, iy] == 0):
            l1.append((ix, iy))
    l2 = []
    for ix, iy in np.ndindex(img2.shape):
        if(img2[ix, iy] == 0):
            l2.append((ix, iy))
    m3 = get_shift(l1, l2)
    l2 = shift_points(l2, m3)
    p3 = generate_points(l1, l2)

    return p3


if __name__ == "__main__":
    path = './src/graphical_interface/letters_dataset/A/skel/2_skel_control_points.png'
    path2 = './src/graphical_interface/letters_dataset/A/skel/0_skel_control_points.png'
    generate_letter(path, path2)
