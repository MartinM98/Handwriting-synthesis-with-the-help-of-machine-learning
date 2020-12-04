import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.file_handler.file_handler import get_filename_without_extention
from src.image_processing.common_functions.common_functions import get_dir
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image
import os


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

    thetas = [0.25 * np.pi, 0.75 * np.pi]
    lamda = 0.16 * np.pi
    for entry in os.scandir(directory):
        if (entry.path.endswith("_skel.png")):
            path2 = get_filename_without_extention(entry.path)
            path = entry.path
            img = get_image(path)
            result = prepare_blank_image(img.shape)
            for theta in thetas:
                filt_real, filt_imag = gabor(
                    img, frequency=1 / lamda, theta=theta)
                cv_image = img_as_ubyte(filt_imag)
                cv_image = invert(cv_image)
                result = np.bitwise_and(result, cv_image)
            if save:
                cv2.imwrite(directory + '/' + path2 + '_control_points.png', result)
            results.append(result)

    return results


if __name__ == '__main__':
    gabor_filter_automated()
