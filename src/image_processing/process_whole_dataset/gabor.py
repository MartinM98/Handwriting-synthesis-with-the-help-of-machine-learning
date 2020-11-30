import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
import os
import sys
from src.file_handler.file_handler import get_file_name


def gabor_filter(directory: str):
    """
    Applies the gabor filter with given paramters to
    all images with the extension png in the directory given
    as parameter to the script.
    Args:
       directory (str): path to the directory that should be processed (Optional).
    """
    if directory is None:
        directory = sys.argv[1]

    thetas = [0.25 * np.pi, 0.75 * np.pi]
    lamda = 0.16 * np.pi
    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = get_file_name()
            path = entry.path
            img = cv2.imread(path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            result = np.zeros(shape=img.shape)
            result = img_as_ubyte(result)
            result = invert(result)
            for theta in thetas:
                filt_real, filt_imag = gabor(
                    img, frequency=1 / lamda, theta=theta)
                cv_image = img_as_ubyte(filt_imag)
                cv_image = invert(cv_image)
                result = np.bitwise_and(result, cv_image)
            cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)


if __name__ == '__main__':
    gabor_filter(None)
