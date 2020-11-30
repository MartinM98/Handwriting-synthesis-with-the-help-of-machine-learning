import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.file_handler.file_handler import get_file_name
from src.image_processing.common_functions.common_functions import get_dir
import os


def gabor_filter_automated():
    """
    Applies the gabor filter with given paramters to
    all images with the extension png in the selected directory and
    saves the results.
    Args:
       None
    """
    directory = get_dir()

    thetas = [0.25 * np.pi, 0.75 * np.pi]
    lamda = 0.16 * np.pi
    for entry in os.scandir(directory):
        if (entry.path.endswith(".png")):
            path2 = get_file_name(entry.path)
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
    gabor_filter_automated()
