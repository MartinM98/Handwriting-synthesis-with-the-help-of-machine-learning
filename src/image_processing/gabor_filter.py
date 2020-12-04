import numpy as np
import cv2
from skimage.filters import gabor
from skimage import img_as_ubyte
from skimage.util import invert
from src.image_processing.common_functions.common_functions import get_image
from src.image_processing.common_functions.common_functions import prepare_blank_image


def gabor_filter(img: np.ndarray = None, path: str = None):
    """
    Applies the gabor filter with given paramters to
    the image.

    Args:
       img (np.ndarray, optional): the image that should be processed.
       path (str, optional): the path to the image that should be
       processed.

    Returns:
        img (np.ndarray): The filtered image.
    """
    thetas = [0.25 * np.pi, 0.75 * np.pi]
    lamda = 0.16 * np.pi
    if img is None:
        img = get_image(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    result = prepare_blank_image(img.shape)
    for theta in thetas:
        filt_real, filt_imag = gabor(
            img, frequency=1 / lamda, theta=theta)
        cv_image = img_as_ubyte(filt_imag)
        cv_image = invert(cv_image)
        result = np.bitwise_and(result, cv_image)

    return result


if __name__ == "__main__":
    if 1 == 2:
        gabor_filter()
