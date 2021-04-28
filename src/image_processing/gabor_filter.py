import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image


def check_point(img: np.ndarray, point: tuple, i: int, x_max: int):
    """
    Checks if the point has a neighbour in the skeleton in the
    given direction
    Args:
       img (np.ndarray, optional): the skeleton image.
       point (tuple): Point that has to be chcked.
       i (int): integer determining direction.
       x_max (int): maximal value of the width coordiante.
    Returns:
        bool: determines if there is a neighbour in the skeleton
        in the given direction.
    """
    result = True
    if i == 1:
        if point[0] != 0:
            result = img[point[0] - 1, point[1]] == 0
    if i == 2:
        if point[0] != (x_max - 1):
            result = img[point[0] + 1, point[1]] == 0
    return result


def shift_point(cv_image: np.ndarray, point: tuple, x: int, x_max: int,):
    """
    Saves current result of the filtering to the final result image.
    The images are accessed as global variables.
    Args:
       cv_image (np.ndarray, optional): the image with selected part
       of control points.
       point (tuple): Point that has to be updated.
       x (int): The shift in the horizontal direction.
       x_max (int): maximal value of the width coordiante.
    """
    if (point[0] != 0) and (point[0] < x_max):
        cv_image[point[0], point[1]] = 255
        cv_image[point[0] + x, point[1]] = 0


def fit_points(img: np.ndarray, cv_image: np.ndarray):
    """
    Fits the control points to the skeleton in the result image.

    Args:
       img (np.ndarray, optional): the skeleton image.
       cv_image (np.ndarray, optional): the image with selected part
       of control points.
    """
    points = []
    left = True
    right = True
    for ix, iy in np.ndindex(cv_image.shape):
        if cv_image[ix, iy] == 0:
            points.append((ix, iy))
    x_max = img.shape[0]
    for point in points:
        if not check_point(img, point, 1, x_max):
            left = False
        if not check_point(img, point, 2, x_max):
            right = False
    x = 0
    if left:
        x = -1
    if right:
        x = 1
    for point in points:
        shift_point(cv_image, point, x, x_max)


def gabor_filter(img: np.ndarray = None, path: str = None, original: bool = False):
    """
    Applies the gabor filter with given paramters to
    the image.

    Args:
       img (np.ndarray, optional): the image that should be processed.
       path (str, optional): the path to the image that should be
       processed.
       original (bool, optional): determines if the control points should
       be original. Otherwise, they are fitted to the skeleton.

    Returns:
        img (np.ndarray): The filtered image.
    """
    thetas = [0.25 * np.pi, 0.75 * np.pi]
    lamda = 0.16 * np.pi
    if img is None:
        img = get_image(path)
    if len(img.shape) > 2:
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = prepare_blank_image(img.shape)
    for theta in thetas:
        filt_real, filt_imag = gabor(
            img, frequency=1 / lamda, theta=theta)
        cv_image = img_as_ubyte(filt_imag)
        cv_image = invert(cv_image)
        if not original:
            fit_points(img, cv_image)
        result = np.bitwise_and(result, cv_image)

    return result
