import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.image_processing.common_functions.common_functions import get_dir_and_file


def nothing(x):
    """
    Does nothing. It is used as sliders handler.
    Args:
       None - x is a surrogate argument.
    """
    pass


def check_point(point: tuple, i: int, x_max: int, y_max: int):
    """
    Checks if the point has a neighbour in the skeleton in the
    given direction
    Args:
       point (tuple): Point that has to be chcked.
       i (int): integer determining direction.
       x_max (int): maximal value of the width coordiante.
       y_max (int): maximal value of the height coordiante.
    Returns:
        bool: determines if there is a neighbour in the skeleton
        in the given direction.
    """
    global cv_image
    global img
    result = True
    if i == 1:
        if point[0] != 0:
            result = img[point[0] - 1, point[1]] == 0
    if i == 2:
        if point[0] != (x_max - 1):
            result = img[point[0] + 1, point[1]] == 0
    if i == 3:
        if point[1] != 0:
            result = img[point[0], point[1] - 1] == 0
    if i == 4:
        if point[1] != (y_max - 1):
            result = img[point[0], point[1] + 1] == 0
    return result


def check_points(points: list):
    """
    Checks for all points if they has neighbours in the skeleton
    in every direction
    Args:
       points (list): The list with points filtered.
    Returns:
        bool: Determines if every point has a neighbour on the LHS.
        bool: Determines if every point has a neighbour on the RHS.
        bool: Determines if every point has a neighbour above.
        bool: Determines if every point has a neighbour on the under.
    """
    global img
    left = True
    right = True
    top = True
    bottom = True
    x_max = img.shape[0]
    y_max = img.shape[1]
    for point in points:
        if not check_point(point, 1, x_max, y_max):
            left = False
        if not check_point(point, 2, x_max, y_max):
            right = False
        if not check_point(point, 3, x_max, y_max):
            top = False
        if not check_point(point, 4, x_max, y_max):
            bottom = False
    return left, right, top, bottom


def print_summary(points: list):
    """
    Prints a summary how many filtered points are on the skeleton
    Args:
        points (list): The list with points filtered.
    """
    global img
    c = 0
    for point in points:
        if img[point[0], point[1]] == 0:
            c += 1
    print(f"SUMMARY\t {len(points)} = {c}")


def process():
    """
    Improves the filtered points so that they would fit to the skeleton.
    """
    global cv_image
    global img
    points = []
    for ix, iy in np.ndindex(cv_image.shape):
        if cv_image[ix, iy] == 0:
            points.append((ix, iy))
    print_summary(points)
    left, right, top, bottom = check_points(points)
    x = 0
    y = 0
    top = False
    bottom = False
    if left:
        x = -1
    if right:
        x = 1
    if top:
        y = -1
    if bottom:
        y = 1
    for point in points:
        update(point, x, y)

    points2 = []
    for ix, iy in np.ndindex(cv_image.shape):
        if cv_image[ix, iy] == 0:
            points2.append((ix, iy))
    print_summary(points2)


def update(point: tuple, x: int, y: int):
    """
    Saves current result of the filtering to the final result image.
    The images are accessed as global variables.
    Args:
       point (tuple): Point that has to be updated.
       x (int): The shift in the horizontal direction.
       y (int): The shift in the vertical direction.
    """
    global cv_image
    if (point[0] != 0) and (point[0] < cv_image.shape[0]):
        cv_image[point[0], point[1]] = 255
        cv_image[point[0] + x, point[1]] = 0


def save(x1, x2):
    """
    Saves current result of the filtering to the final result image.
    The images are accessed as global variables.
    Args:
       None - x1 and x2 are surrogate arguments.
    """
    global result
    global img
    global cv_image
    result = np.bitwise_and(result, cv_image)


def save_shifted(x1, x2):
    """
    Saves current result of the filtering to the final result image.
    The images are accessed as global variables.
    Args:
       None - x1 and x2 are surrogate arguments.
    """
    global result
    global img
    global cv_image
    process()
    result = np.bitwise_and(result, cv_image)


def reset(x1, x2):
    """
    Clear the result image.
    """
    global result
    global img
    result = np.zeros(shape=img.shape)
    result = img_as_ubyte(result)
    result = invert(result)


def reset_skel(x1, x2):
    """
    Clear the result image with the skeleton included
    in the result image.
    """
    global result
    global img
    result = np.zeros(shape=img.shape)
    result = img_as_ubyte(result)
    result = invert(result)
    result = np.bitwise_and(result, img)


def gabor_filter():
    """
    Main function. Creates GUI for changing the filtering parmeters,
    shows and saves the result.
    Args:
       None
    """
    global result
    global cv_image
    directory, path2, path = get_dir_and_file()
    img2 = np.zeros((300, 512, 3), np.uint8)
    cv2.namedWindow('trackbar')
    global img
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = np.zeros(shape=img.shape)
    result = img_as_ubyte(result)
    result = invert(result)
    # result = np.bitwise_and(result, img)

    cv2.createTrackbar('theta', 'trackbar', 25, 300, nothing)
    cv2.createTrackbar('lamda', 'trackbar', 16, 300, nothing)
    cv2.createTrackbar('offset', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('n_stds', 'trackbar', 3, 300, nothing)
    cv2.createTrackbar('bandwidth', 'trackbar', 10, 300, nothing)
    cv2.createTrackbar('sigma_x', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('sigma_y', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('cval', 'trackbar', 0, 300, nothing)
    cv2.createTrackbar('cval', 'trackbar', 0, 300, nothing)
    cv2.createButton('save crl points', save, [''], cv2.QT_PUSH_BUTTON)
    cv2.createButton('save crl points in skel', save_shifted, [''], cv2.QT_PUSH_BUTTON)
    cv2.createButton('reset', reset, [''], cv2.QT_PUSH_BUTTON)
    cv2.createButton('reset skel', reset_skel, [''], cv2.QT_PUSH_BUTTON)
    while(1):
        cv2.imshow('trackbar', img2)
        k = cv2.waitKey(1) & 0xFF
        if k == 97:
            break

        theta = cv2.getTrackbarPos('theta', 'trackbar') * 0.01 * np.pi
        lamda = cv2.getTrackbarPos('lamda', 'trackbar') * 0.01 * np.pi
        offset = cv2.getTrackbarPos('offset', 'trackbar') * 0.1
        bandwidth = cv2.getTrackbarPos('bandwidth', 'trackbar') * 0.1
        sigma_x = cv2.getTrackbarPos('sigma_x', 'trackbar') * 0.1
        sigma_y = cv2.getTrackbarPos('sigma_y', 'trackbar') * 0.1
        cval = cv2.getTrackbarPos('cval', 'trackbar') * 0.1
        n_stds = cv2.getTrackbarPos('n_stds', 'trackbar')
        if bandwidth == 0:
            continue
        img = cv2.imread(path)

        plt.imshow(img, cmap='gray')
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if sigma_x == 0 or sigma_y == 0:
            filt_real, filt_imag = gabor(
                img, frequency=1 / lamda, theta=theta, n_stds=n_stds, offset=offset, bandwidth=bandwidth, cval=cval)
        else:
            filt_real, filt_imag = gabor(img, frequency=1 / lamda, theta=theta, n_stds=n_stds,
                                         offset=offset, bandwidth=bandwidth, sigma_x=sigma_x, sigma_y=sigma_y, cval=cval)

        cv2.imshow('Original Img.', img)
        cv_image = img_as_ubyte(filt_imag)
        cv_image = invert(cv_image)
        cv_image3 = img_as_ubyte(filt_real)
        cv_image3 = invert(cv_image3)

        size = (200, 200)
        cv_image2 = cv2.resize(cv_image, size)
        cv_image4 = cv2.resize(cv_image3, size)

        cv2.imshow('Filtered imag', cv_image2)
        cv2.imshow('Filtered real', cv_image4)
        result2 = cv2.resize(result, (300, 300))
        cv2.imshow('Result', result2)

    cv2.destroyAllWindows()
    cv2.waitKey()
    cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)


if __name__ == '__main__':
    gabor_filter()
