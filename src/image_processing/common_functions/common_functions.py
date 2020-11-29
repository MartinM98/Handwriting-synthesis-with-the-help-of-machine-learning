from tkinter import filedialog, Tk
import cv2
import math
import numpy as np
from skimage import img_as_ubyte
from skimage.util import invert
from src.file_handler.file_handler import get_dir_path, get_file_name


def get_dir_and_file():
    """
    Opens a filedialog and returns the directory in which
    the selected file resides, the filename without extension
    and the absoulte path to the filename

    Args:
        None

    Returns:
        directory (str): directory in which the selected file resides
        path2 (str): selected filename without extension
        root.filename (str): path to the selected file

    """
    root = Tk()
    root.withdraw()
    root.filename = filedialog.askopenfilename(initialdir=".", title="Select file", filetypes=(
        ("png files", "*.png"), ("all files", "*.*")))
    directory = get_dir_path(root.filename)
    path2 = get_file_name(root.filename)
    root.destroy()
    return directory, path2, root.filename


def get_dir():
    """
    Opens a filedialog and returns the selected directory.

    Args:
        None

    Returns:
        directory (str): selected directory
    """
    root = Tk()
    root.withdraw()
    root.directory = filedialog.askdirectory(initialdir=".")
    directory = root.directory
    root.destroy()
    return directory


def process_part(image: np.ndarray, x1: int, y1: int, x2: int, y2: int):
    """
    Process a part of an image returning
    list containing locations of points/pixels
    which are black (have value 0)

    Args:
        image (np.ndarray): the whole cv2 image.
        x1 (int): width value of the left edge of the selected part of the image.
        y1 (int): height value of the upper edge of the selected part of the image.
        x2 (int): width value of the right edge of the selected part of the image.
        y2 (int): height value of the lower edge of the selected part of the image.

    Returns:
        points (list): list containing locations of points/pixels
            which are black (have value 0).
    """
    points = []
    for y in range(y1, y2 + 1):
        for x in range(x1, x2 + 1):
            point = []
            if image[x, y] == 0:
                point.append(x)
                point.append(y)
                points.append(point)
    return points


def get_image(path: str):
    """
    Reads and returns an cv2 image saved in the passed path.

    Args:
        path (str): absoulte or relative path to the image.

    Returns:
        img (np.ndarray): read image
    """
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(f"Size: {img.shape}")
    return img


def get_dimensions(img: np.ndarray, n: int):
    """
    Computes and returns steps that divides the image
    into n x n parts and returns dimensions
    of the image as well as the steps in both
    directions
    Args:
       img (np.ndarray): cv2 image.
       n (int): the number of subparts in each direction.

    Returns:
        x_step (int): x step that is the horizontal
            length of the subpart of the image.
        width (int): The width of the image.
        y_step (int): y step that is the vertical length
            of the subpart of the image.
        height (int): The height of the image.
    """
    width = img.shape[0]
    height = img.shape[1]
    x_step = math.ceil(width / n)
    y_step = math.ceil(height / n)
    return width, height, x_step, y_step


def get_box(x: int, x_step: int, width: int, y: int, y_step: int, height: int):
    """
    Computes and returns the next box based on initial x,y and steps.
    The functions truncates the points if they would
    be outside the image dimensions.
    Args:
       x (int): Initial x.
       x_step (int): x step that is the horizontal
           length of the subpart of the image.
       width (int): The width of the image.
       y (int): Initial y.
       y_step (int): y step that is the vertical length
           of the subpart of the image.
       height (int): The height of the image.

    Returns:
        x1 (int): width value of the left edge of the selected part of the image.
        y1 (int): height value of the upper edge of the selected part of the image.
        x2 (int): width value of the right edge of the selected part of the image.
        y2 (int): height value of the lower edge of the selected part of the image.
    """
    x1 = x
    x2 = x + x_step - 1
    if x2 >= width:
        x2 = width - 1
    y1 = y
    y2 = y + y_step - 1
    if y2 >= height:
        y2 = height - 1
    return x1, x2, y1, y2


def prepare_blank_image(img: np.ndarray):
    """
    Creates and returns blank image (with all white pixels)
    based on dimension of the passed image.
    Args:
       img (np.ndarray): cv2 image.

    Returns:
        img (np.ndarray): prepared cv2 blank image.
    """
    img2 = np.zeros(shape=img.shape)
    img2 = img_as_ubyte(img2)
    img2 = invert(img2)
    return img2


def resize_and_show_images(img: np.ndarray, img2: np.ndarray):
    """
    Resizes given images to be better visible and shows them.
    Args:
       img (np.ndarray): cv2 image.
       img2 (np.ndarray): cv2 image.
    """
    size = (500, 500)
    img = cv2.resize(img, size)
    img3 = cv2.resize(img2, size)
    cv2.imshow('Original', img)
    cv2.imshow('Limited', img3)
    cv2.waitKey()


def get_parts(img, n, parts):
    """
    Creates parts of the given image dividing it into n x n grid.
    They are appended to the given list of parts.
    Args:
       img (np.ndarray): cv2 image.
       img2 (np.ndarray): cv2 image.
    """
    width, height, x_step, y_step = get_dimensions(img, n)
    for y in range(0, height, y_step):
        for x in range(0, width, x_step):
            x1, x2, y1, y2 = get_box(x, x_step, width, y, y_step, height)
            parts.append(process_part(img, x1, y1, x2, y2))
